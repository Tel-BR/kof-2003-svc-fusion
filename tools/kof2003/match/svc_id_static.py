"""Static inventory of what SVC Chaos reads by a fighter's ID (wayfinder ticket 28).

MAME's taps and watchpoints cannot see work-RAM reads (see svc_id_readers.lua), so the readers
are found in the decrypted program instead: sweep the 68000 code, list every instruction that
touches the ID fields of a fighter object, and follow the loaded ID forward to the tables it
indexes.

    py -3 -m match.svc_id_static PROGRAM OUT_DIR [--end 0x80000]

PROGRAM is the decrypted main CPU file (word-swapped as MAME exports it, or already in 68000
order). OUT_DIR must be under private/: the two TSV files it gets carry disassembly text, which is
game data. Needs `pip install capstone`. What goes into docs is only addresses, sizes and counts.
"""
import argparse
import re
import sys
from collections import Counter
from pathlib import Path
from typing import NamedTuple, Optional

from capstone import CS_ARCH_M68K, CS_MODE_BIG_ENDIAN, CS_MODE_M68K_000, Cs

# Offsets in an SVC fighter object that carry the fighter ID (ticket 28): the ID byte (+$71, the
# low byte of the word at +$70), the team-slot copy (+$77), a second copy (+$1D6), and the ID
# doubled (the word at +$180, low byte +$181, a word offset into a table). The word at +$70 itself
# is every object's type or state (a menu counter, an effect's kind), so it is only followed where
# asked with --also, and only code that runs on fighter objects tells it apart.
ID_FIELDS = (0x71, 0x77, 0x1D6, 0x180, 0x181, 0x182, 0x184, 0x186)
# The creation code stores the ID times 2, 4, 8 and 16 as words at +$180, +$182, +$184 and +$186,
# ready to index tables; a read of one of them is an ID read with that scale already applied.
PREMULTIPLIED = {0x180: 2, 0x181: 2, 0x182: 4, 0x184: 8, 0x186: 16}

_TESTS = {"cmp", "cmpi", "cmpa", "tst", "btst"}
_ENDS_ROUTINE = {"rts", "rte", "jmp", "bra"}
_KEEPS_VALUE = {"cmp", "cmpi", "cmpa", "tst", "btst", "andi", "and", "ext"}
_MEM = re.compile(r"^(-?)(?:\$([0-9a-f]+))?\((a[0-7]|pc)(?:, ([ad][0-7])\.([wl]))?\)([+]?)$")
_ABS = re.compile(r"^\$([0-9a-f]+)\.[wl]$")
_IMM = re.compile(r"^#\$([0-9a-f]+)$")
_REG_D = re.compile(r"^d[0-7]$")


class Insn(NamedTuple):
    address: int
    size: int
    mnemonic: str
    width: str
    operands: tuple


class Use(NamedTuple):
    address: int
    field: int
    role: str          # read, write or test
    indexed: bool
    immediate: Optional[int]


class TableRead(NamedTuple):
    field: int
    site: int          # where the ID was loaded
    access: int        # the instruction that used it
    kind: str          # table (indexed read), identity (compared with a literal ID), call
    base: Optional[int]
    scale: int
    width: str
    immediate: Optional[int] = None
    callee: Optional[int] = None
    argument: Optional[int] = None   # d1 at a call, usually the row size


def normalise_program(raw):
    """The program in 68000 order. MAME's export stores each 16-bit word byte-swapped."""
    def vector_ok(data):
        return 0x100000 <= int.from_bytes(data[:4], "big") <= 0x10FFFF
    if vector_ok(raw):
        return bytes(raw)
    swapped = bytearray(raw)
    swapped[0::2], swapped[1::2] = raw[1::2], raw[0::2]
    if vector_ok(swapped):
        return bytes(swapped)
    raise ValueError("the reset vector (stack pointer) is not work RAM in either byte order")


def _split_operands(text):
    parts, depth, current = [], 0, ""
    for char in text:
        if char == "," and depth == 0:
            parts.append(current.strip())
            current = ""
            continue
        depth += (char == "(") - (char == ")")
        current += char
    if current.strip():
        parts.append(current.strip())
    return tuple(parts)


def sweep(code, start=0, end=None):
    """Linear sweep from `start`; a word that is not an instruction (data) is skipped."""
    disassembler = Cs(CS_ARCH_M68K, CS_MODE_M68K_000 | CS_MODE_BIG_ENDIAN)
    end = len(code) if end is None else min(end, len(code))
    out, pc = [], start
    while pc < end:
        decoded = next(disassembler.disasm(bytes(code[pc:pc + 12]), pc, 1), None)
        if decoded is None:
            pc += 2
            continue
        name, _, width = decoded.mnemonic.partition(".")
        out.append(Insn(pc, decoded.size, name, width, _split_operands(decoded.op_str)))
        pc += decoded.size
    return out


def _field_operand(text):
    """(displacement, indexed, base register) of a (d,An) or (d,An,Xn) operand, positive displacement."""
    match = _MEM.match(text)
    if not match or match.group(3) == "pc" or match.group(1) or match.group(2) is None:
        return None
    return int(match.group(2), 16), match.group(4) is not None, match.group(3)


def field_uses(insns, fields):
    """Uses of the given offsets. An entry is a displacement, or ("a5", displacement) to match
    only that base register (the team slots are addressed from the RAM base in a5)."""
    uses = []
    for insn in insns:
        for position, text in enumerate(insn.operands):
            found = _field_operand(text)
            if not found or not (found[0] in fields or (found[2], found[0]) in fields):
                continue
            if insn.mnemonic in _TESTS:
                role = "test"
            elif position == len(insn.operands) - 1:
                role = "write"
            else:
                role = "read"
            immediate = None
            if role == "test" and insn.operands and _IMM.match(insn.operands[0]):
                immediate = int(insn.operands[0][2:], 16)
            uses.append(Use(insn.address, found[0], role, found[1], immediate))
    return uses


def summarise(uses):
    return dict(Counter((use.field, use.role) for use in uses))


def _constant(text):
    for pattern in (_ABS, _IMM):
        match = pattern.match(text)
        if match:
            return int(match.group(1), 16)
    match = _MEM.match(text)
    if match and match.group(3) == "pc" and match.group(4) is None and match.group(2):
        return int(match.group(2), 16)
    return None


def _sets_base(insn):
    if insn.mnemonic in ("lea", "movea") and len(insn.operands) == 2 and insn.operands[1].startswith("a"):
        value = _constant(insn.operands[0])
        if value is not None:
            return insn.operands[1], value
    return None


def _bases_before(insns, k, reach=16):
    bases = {}
    for insn in reversed(insns[max(0, k - reach):k]):
        if insn.mnemonic in _ENDS_ROUTINE:
            break
        found = _sets_base(insn)
        if found and found[0] not in bases:
            bases[found[0]] = found[1]
    return bases


def _small_constant(insn):
    """(register, value) when the instruction loads a small literal into a data register."""
    if insn.mnemonic in ("moveq", "move") and len(insn.operands) == 2 and _REG_D.match(insn.operands[1]):
        match = _IMM.match(insn.operands[0])
        if match:
            return insn.operands[1], int(match.group(1), 16)
    return None


def _follow(insns, k, field, window):
    load = insns[k]
    reg = load.operands[-1]
    scale, bases, pointers, found = PREMULTIPLIED.get(field, 1), _bases_before(insns, k), {}, []
    constants = {}

    def note(insn, kind, base, width=None, **extra):
        found.append(TableRead(field, load.address, insn.address, kind, base, scale,
                               width or insn.width, **extra))

    for insn in insns[k + 1:k + 1 + window]:
        for text in insn.operands:
            match = _MEM.match(text)
            if not match:
                continue
            area, index = match.group(3), match.group(4)
            if index == reg:
                if area == "pc":
                    base = int(match.group(2), 16)
                elif area in bases:
                    base = bases[area] + int(match.group(2) or "0", 16)
                else:
                    base = None
                note(insn, "table", base)
            elif area in pointers:
                base, pointer_scale = pointers.pop(area)
                found.append(TableRead(field, load.address, insn.address, "table", base,
                                       pointer_scale, insn.width))
        mnemonic, ops = insn.mnemonic, insn.operands
        if (loaded := _small_constant(insn)) and loaded[0] != reg:
            constants[loaded[0]] = loaded[1]
        if mnemonic == "adda" and ops[0] == reg and ops[1].startswith("a"):
            pointers[ops[1]] = (bases.get(ops[1]), scale)
        if (based := _sets_base(insn)):
            bases[based[0]] = based[1]
            pointers.pop(based[0], None)
        if mnemonic in ("cmp", "cmpi") and ops[-1] == reg and _IMM.match(ops[0]):
            note(insn, "identity", None, immediate=int(ops[0][2:], 16))
        if mnemonic in ("jsr", "bsr"):
            note(insn, "call", bases.get("a0"), callee=_constant(ops[0]), argument=constants.get("d1"))
            break
        if mnemonic in _ENDS_ROUTINE:
            break
        if len(ops) == 2 and ops[1] == reg:
            if mnemonic == "add" and ops[0] == reg:
                scale *= 2
            elif mnemonic in ("lsl", "asl") and _IMM.match(ops[0]):
                scale <<= int(ops[0][2:], 16)
            elif mnemonic in ("mulu", "muls") and _IMM.match(ops[0]):
                scale *= int(ops[0][2:], 16)
            elif mnemonic not in _KEEPS_VALUE:
                break
        elif ops and ops[-1] == reg and mnemonic not in _KEEPS_VALUE:
            break
    return found


def table_reads(insns, uses, window=30):
    position = {insn.address: k for k, insn in enumerate(insns)}
    reads = []
    for use in uses:
        insn = insns[position[use.address]]
        if use.role == "read" and not use.indexed and _REG_D.match(insn.operands[-1]):
            reads.extend(_follow(insns, position[use.address], use.field, window))
    return reads


def routine_start(insns, address):
    """First instruction after the last rts/rte/jmp/bra before `address` (a heuristic)."""
    start = insns[0].address
    for insn in insns:
        if insn.address >= address:
            break
        if insn.mnemonic in _ENDS_ROUTINE:
            start = insn.address + insn.size
    return start


def _write_reports(insns, uses, reads, out_dir):
    by_address = {insn.address: insn for insn in insns}
    with open(out_dir / "uses.tsv", "w") as out:
        out.write("address\tfield\trole\tindexed\timmediate\troutine\ttext\n")
        for use in uses:
            insn = by_address[use.address]
            immediate = "" if use.immediate is None else f"{use.immediate:X}"
            out.write(f"{use.address:06X}\t{use.field:X}\t{use.role}\t{int(use.indexed)}\t{immediate}\t"
                      f"{routine_start(insns, use.address):06X}\t{insn.mnemonic}.{insn.width} {','.join(insn.operands)}\n")
    with open(out_dir / "tables.tsv", "w") as out:
        out.write("field\tsite\taccess\tkind\tbase\tscale\twidth\timmediate\tcallee\targument\n")
        for read in reads:
            fmt = lambda value: "" if value is None else f"{value:X}"  # noqa: E731
            out.write(f"{read.field:X}\t{read.site:06X}\t{read.access:06X}\t{read.kind}\t{fmt(read.base)}\t"
                      f"{read.scale:X}\t{read.width}\t{fmt(read.immediate)}\t{fmt(read.callee)}\t{fmt(read.argument)}\n")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("program", type=Path)
    parser.add_argument("out_dir", type=Path)
    parser.add_argument("--end", type=lambda text: int(text, 0), default=0x80000,
                        help="stop the sweep here (the code in the SVC program ends at 0x80000; what follows is data)")
    parser.add_argument("--also", default="", help="more offsets to follow, comma separated; BASE:OFFSET limits one to a register, e.g. 0x70,a5:0x2c34")
    parser.add_argument("--range", dest="span", default="",
                        help="keep only uses in START:END (hex or decimal), e.g. 0x17C00:0x17F00")
    args = parser.parse_args(argv)
    if "private" not in args.out_dir.resolve().parts:
        parser.error("OUT_DIR must be under private/: the reports carry game disassembly")
    code = normalise_program(args.program.read_bytes())
    insns = sweep(code, 0, args.end)
    fields = set(ID_FIELDS)
    for item in filter(None, args.also.split(",")):
        base, _, offset = item.rpartition(":")
        fields.add((base, int(offset, 0)) if base else int(offset, 0))
    uses = field_uses(insns, fields)
    if args.span:
        low, high = (int(item, 0) for item in args.span.split(":"))
        uses = [use for use in uses if low <= use.address < high]
    reads = table_reads(insns, uses)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    _write_reports(insns, uses, reads, args.out_dir)
    print(f"{len(insns)} instructions swept, {len(uses)} uses, {len(reads)} followed reads")
    for (field, role), count in sorted(summarise(uses).items()):
        print(f"  +${field:X} {role}: {count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
