"""Map the fighter ID that selects a per-fighter routine table through the presentation map.

Run after wire_slot_lookups.py. It writes a new private program image; the input
is never changed. Two dispatchers ($2B30E and $2B432) pick a fighter's own table of
routines by the fighter ID and call one of them with `jsr`: they index a 37-entry
table of pointers (at $2B336 and $2B45A) with `4 * (ID & $3F)`. For the imported
`$30` the index ran past the end of the table, so the call landed in other data
instead of original Kyo's routines. In the recorded Orochinagi replay the clone
kept the flames of the move on screen for the rest of the match, while the same
input with original Kyo removed them. The three instructions that compute the index
(`and.w ($1E,A4),D1` and two `add.w D1,D1`) are rerouted to one short routine that
maps the ID through the 64-byte presentation map at $53100 first, so the imported
fighter uses its source fighter's routines. Original IDs map to themselves.

It does not give an imported fighter routines of its own; that needs a real table
entry. The five other places with the same index arithmetic read directory tables
that wire_slot_lookups.py and the table tools already extend.
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
PRESENTATION_TABLE = 0x53100
# and.w ($1e,a4),d1 ; add.w d1,d1 ; add.w d1,d1, right after moveq #$3f,d1.
SITES = (0x2B314, 0x2B438)
SITE_BYTES = bytes.fromhex('c26c001ed241d241')
MOVEQ_3F = bytes.fromhex('723f')
JSR_ABS, NOP, RTS = b'\x4e\xb9', b'\x4e\x71', b'\x4e\x75'
# Free fixed space after the intro-opponent routine ($53240-$5327F).
TRAMPOLINE = 0x53280
TRAMPOLINE_END = 0x532C0
TRAMPOLINE_CODE = (
    bytes.fromhex('c26c001e') +    # and.w ($1e,a4),d1           (displaced)
    bytes.fromhex('48e70040') +    # movem.l a1,-(a7)
    bytes.fromhex('43f9') + PRESENTATION_TABLE.to_bytes(4, 'big') +   # lea TABLE,a1
    bytes.fromhex('12311000') +    # move.b (0,a1,d1.w),d1       map the fighter ID
    bytes.fromhex('4cdf0200') +    # movem.l (a7)+,a1
    bytes.fromhex('d241d241') +    # add.w d1,d1 ; add.w d1,d1   (displaced)
    RTS)


def map_fighter_handlers(data):
    result = bytearray(data)
    table = result[PRESENTATION_TABLE:PRESENTATION_TABLE + 64]
    if (table[:FIRST_UNUSED_ID] != bytes(range(FIRST_UNUSED_ID)) or
            table[IMPORTED_ID] >= FIRST_UNUSED_ID or table[IMPORTED_ID] == IMPORTED_ID):
        raise ValueError('presentation map is missing; run wire_slot_lookups.py first')
    for site in SITES:
        if (result[site:site + len(SITE_BYTES)] != SITE_BYTES or
                result[site - len(MOVEQ_3F):site] != MOVEQ_3F):
            raise ValueError(f'unexpected routine index code at 0x{site:X}')
    if len(TRAMPOLINE_CODE) > TRAMPOLINE_END - TRAMPOLINE:
        raise ValueError('routine index routine does not fit')
    if result[TRAMPOLINE:TRAMPOLINE_END] != b'\xff' * (TRAMPOLINE_END - TRAMPOLINE):
        raise ValueError(f'routine index routine area 0x{TRAMPOLINE:X} is not empty')
    result[TRAMPOLINE:TRAMPOLINE + len(TRAMPOLINE_CODE)] = TRAMPOLINE_CODE
    for site in SITES:
        result[site:site + len(SITE_BYTES)] = JSR_ABS + TRAMPOLINE.to_bytes(4, 'big') + NOP
    return result


def prepare(source, destination, expected_hash):
    private = PRIVATE.resolve(strict=True)
    source, destination = source.resolve(strict=True), destination.resolve()
    if not source.is_relative_to(private) or not destination.is_relative_to(private):
        raise ValueError('input and output must be inside private/')
    data = source.read_bytes()
    if len(data) != PROGRAM_SIZE or hashlib.sha256(data).hexdigest() != expected_hash.lower():
        raise ValueError('program size or SHA-256 does not match the supplied identity')
    result = map_fighter_handlers(data)
    with destination.open('xb') as output:
        output.write(result)
    return hashlib.sha256(result).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--sha256', required=True, help='expected SHA-256 of the input')
    args = parser.parse_args()
    try:
        digest = prepare(args.source, args.destination, args.sha256)
    except (OSError, ValueError) as error:
        print(f'Cannot map the fighter routine index: {error}', file=sys.stderr)
        return 1
    print(f'Mapped the fighter routine index; SHA-256 {digest}.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
