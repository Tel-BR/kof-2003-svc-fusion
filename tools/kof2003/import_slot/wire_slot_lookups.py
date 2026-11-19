"""Wire the remaining fighter-ID lookups of a relocated program image to ID $30.

Run after relocate_action_tables.py. It writes a new private image; the input
is never changed. Each change is checked against the expected bytes first:

* raise four ID guards that still stop at $24/$25 in front of tables that are
  already relocated to 64 rows;
* move the two 37-entry special-intro tables to 64 rows in unused fixed space,
  repoint their readers and copy the source fighter's entry to $30;
* copy the source fighter's entry to $30 in 64-entry lookup tables whose
  entries above $24 hold a shared default;
* route the selection-screen and in-fight name-plate lookups through a shared
  64-entry presentation map, so $30 shows the source fighter's name, portraits
  and team-position art (those lookups only handle IDs up to $24).

It does not place frame data, extend per-opponent tables or add sound data.
"""
import argparse
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PRIVATE = ROOT / 'private'
PROGRAM_SIZE = 0x900000
IMPORTED_ID = 0x30
FIRST_UNUSED_ID = 0x25

# (offset of the 16-bit immediate, old value, new value); each is a cmpi.w.
GUARDS = ((0x166AE, 0x24, 0x3F), (0x240F6, 0x25, 0x40),
          (0x2412A, 0x24, 0x3F), (0x27E0C, 0x24, 0x3F))
CMPI_W_D0 = b'\x0c\x40'

# (37-entry table, 4-byte rows, new location, absolute references)
INTRO_TABLES = ((0xA5DB6, 0x52C00, (0x407EA, 0x40866)),
                (0xA5E4A, 0x52D00, (0x409E8, 0x40C70)))
INTRO_ROW = 4
NEW_ROWS = 64

# 64-entry tables: (file offset, entry size). Entries $25-$3F share a default.
DEFAULT_TABLES = ((0x79672, 4), (0x79772, 4), (0xB8250, 4),
                  (0x62B9AC, 4), (0x79872, 2), (0x798F2, 2))
# Word-offset table with header room for more entries than its 37 fighters.
HEADER_TABLE = 0xB3204

# Presentation map in unused fixed space ($52E00-$52E11 holds other proxy code, so start
# at $53100): a 64-byte identity table with $30 pointing at the source fighter, a
# 16-byte lookup routine and one small trampoline per displaced instruction group.
PRESENTATION_TABLE = 0x53100
PRESENTATION_ROUTINE = 0x53140
PRESENTATION_CODE = 0x53150
PRESENTATION_END = 0x53200
HIDDEN_FROM = 0x22  # IDs $22-$24 are hidden entries of the original roster
JSR_ABS, NOP, RTS = b'\x4e\xb9', b'\x4e\x71', b'\x4e\x75'
ANDI_3F = b'\x02\x40\x00\x3f'  # andi.w #$3f,d0
# (bytes before the lookup, bytes after it, call sites). The displaced code is
# `before + after`; the lookup maps d0 in between. Sites are four selection-screen
# readers (name, portrait, thumbnail, palette group), the order-screen portrait and
# group readers and the in-fight name-plate writer.
PRESENTATION_SITES = (
    (ANDI_3F, bytes.fromhex('0c400022'), (0x9042, 0x9124, 0x91FE, 0x9338)),
    (ANDI_3F, bytes.fromhex('06400100'), (0x9E00,)),
    (ANDI_3F, bytes.fromhex('80fc0003'), (0x9F26,)),
    (bytes.fromhex('703fc010'), bytes.fromhex('d040'), (0x1F886,)),
)


def word(data, offset):
    return int.from_bytes(data[offset:offset + 2], 'big')


def long(data, offset):
    return int.from_bytes(data[offset:offset + 4], 'big')


def map_presentation(result, fighter_id):
    """Insert the presentation map and reroute its call sites (in place)."""
    if fighter_id >= HIDDEN_FROM:
        raise ValueError('source fighter has no presentation: IDs $22-$24 are hidden entries')
    size = PRESENTATION_END - PRESENTATION_TABLE
    if result[PRESENTATION_TABLE:PRESENTATION_END] != b'\xff' * size:
        raise ValueError(f'presentation map area 0x{PRESENTATION_TABLE:X} is not empty')
    for before, after, sites in PRESENTATION_SITES:
        for site in sites:
            if result[site:site + len(before) + len(after)] != before + after:
                raise ValueError(f'unexpected presentation code at 0x{site:X}')
    table = bytearray(range(NEW_ROWS))
    table[IMPORTED_ID] = fighter_id
    result[PRESENTATION_TABLE:PRESENTATION_TABLE + NEW_ROWS] = table
    # move.l a0,-(a7); lea TABLE,a0; move.b (a0,d0.w),d0; movea.l (a7)+,a0; rts
    routine = (b'\x2f\x08\x41\xf9' + PRESENTATION_TABLE.to_bytes(4, 'big') +
               b'\x10\x30\x00\x00\x20\x5f' + RTS)
    result[PRESENTATION_ROUTINE:PRESENTATION_ROUTINE + len(routine)] = routine
    call = JSR_ABS + PRESENTATION_ROUTINE.to_bytes(4, 'big')
    cursor = PRESENTATION_CODE
    for before, after, sites in PRESENTATION_SITES:
        trampoline = before + call + after + RTS
        if cursor + len(trampoline) > PRESENTATION_END:
            raise ValueError('presentation trampolines do not fit')
        result[cursor:cursor + len(trampoline)] = trampoline
        length = len(before) + len(after)
        for site in sites:
            patch = JSR_ABS + cursor.to_bytes(4, 'big') + NOP * ((length - 6) // 2)
            result[site:site + length] = patch
        cursor += len(trampoline)


def wire(data, fighter_id):
    result = bytearray(data)
    map_presentation(result, fighter_id)
    for immediate, old, new in GUARDS:
        if result[immediate - 2:immediate] != CMPI_W_D0 or word(result, immediate) != old:
            raise ValueError(f'unexpected ID guard at 0x{immediate - 2:X}')
        result[immediate:immediate + 2] = new.to_bytes(2, 'big')
    for table, new, references in INTRO_TABLES:
        size = INTRO_ROW * NEW_ROWS
        if result[new:new + size] != b'\xff' * size:
            raise ValueError(f'destination 0x{new:X} is not empty')
        for reference in references:
            if long(result, reference) != table:
                raise ValueError(f'unexpected intro table reference at 0x{reference:X}')
        # Preserve the old indexed reads, as the other relocations do.
        result[new:new + size] = data[table:table + size]
        source = table + fighter_id * INTRO_ROW
        result[new + IMPORTED_ID * INTRO_ROW:new + (IMPORTED_ID + 1) * INTRO_ROW] = \
            data[source:source + INTRO_ROW]
        for reference in references:
            result[reference:reference + 4] = new.to_bytes(4, 'big')
    for table, size in DEFAULT_TABLES:
        entries = [bytes(result[table + i * size:table + (i + 1) * size]) for i in range(NEW_ROWS)]
        if len(set(entries[FIRST_UNUSED_ID:])) != 1:
            raise ValueError(f'table 0x{table:X} has no shared default above $24')
        if entries[fighter_id] == entries[FIRST_UNUSED_ID]:
            raise ValueError(f'table 0x{table:X} has no own entry for the source fighter')
        start = table + IMPORTED_ID * size
        result[start:start + size] = entries[fighter_id]
    header = word(result, HEADER_TABLE)
    if header < 2 * (IMPORTED_ID + 1) or word(result, HEADER_TABLE + 2 * IMPORTED_ID) != 0:
        raise ValueError('command-to-action header has no free entry for $30')
    if any(word(result, HEADER_TABLE + 2 * i) == 0 for i in range(37)):
        raise ValueError('command-to-action header is not the expected layout')
    result[HEADER_TABLE + 2 * IMPORTED_ID:HEADER_TABLE + 2 * IMPORTED_ID + 2] = \
        result[HEADER_TABLE + 2 * fighter_id:HEADER_TABLE + 2 * fighter_id + 2]
    return result


def prepare(source, destination, expected_hash, fighter_id):
    private = PRIVATE.resolve(strict=True)
    source, destination = source.resolve(strict=True), destination.resolve()
    if not source.is_relative_to(private) or not destination.is_relative_to(private):
        raise ValueError('input and output must be inside private/')
    if not 0 <= fighter_id < 37:
        raise ValueError('fighter ID must be an original ID from 0 to 36')
    data = source.read_bytes()
    if len(data) != PROGRAM_SIZE or hashlib.sha256(data).hexdigest() != expected_hash.lower():
        raise ValueError('program size or SHA-256 does not match the supplied identity')
    result = wire(data, fighter_id)
    with destination.open('xb') as output:
        output.write(result)
    return hashlib.sha256(result).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--sha256', required=True, help='expected SHA-256 of the input')
    parser.add_argument('--fighter-id', required=True, type=lambda value: int(value, 0))
    args = parser.parse_args()
    try:
        digest = prepare(args.source, args.destination, args.sha256, args.fighter_id)
    except (OSError, ValueError) as error:
        print(f'Cannot wire lookups: {error}', file=sys.stderr)
        return 1
    print(f'Wired ID lookups; SHA-256 {digest}. Frame placement and opponent data remain open.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
