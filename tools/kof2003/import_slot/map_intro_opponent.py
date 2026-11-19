"""Map the other fighter's ID in the special-intro row scan through the presentation map.

Run after wire_slot_lookups.py. It writes a new private program image; the input
is never changed. The special-intro selection (routine at $40BCA, reached from
$409E8 and $407EA/$40866 through the tables at $52D00 and $52C00) reads the other
fighter's ID at $40BE2 and looks for it, as a literal ID or through a group code,
in the row of the fighter whose intro is being chosen. Rival pairs are written that
way: the row of Iori Yagami names Kyo Kusanagi ($1E), so facing the imported $30
gave Iori the default intro and every later frame of the fight differed from the
same fight against original Kyo. The eight bytes of the read and the next
instruction are rerouted to a short routine that repeats them with the ID mapped
through the 64-byte presentation map at $53100, so the imported fighter is
recognised as its source fighter. Original IDs map to themselves.

It does not decide which rivals an imported fighter should have; the map entry of
$30 chooses that, and it is also the presentation source.
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
# move.b ($1f,a3),d1 ; move.w #3,d7 -- the other fighter's ID, then the row length.
SITE = 0x40BE2
SITE_BYTES = bytes.fromhex('122b001f3e3c0003')
JSR_ABS, NOP, RTS = b'\x4e\xb9', b'\x4e\x71', b'\x4e\x75'
# Free fixed space right after the victory-screen routine ($53200-$5323F).
TRAMPOLINE = 0x53240
TRAMPOLINE_END = 0x53280
TRAMPOLINE_CODE = (
    bytes.fromhex('122b001f') +    # move.b ($1f,a3),d1          (displaced)
    bytes.fromhex('48e70040') +    # movem.l a1,-(a7)
    bytes.fromhex('43f9') + PRESENTATION_TABLE.to_bytes(4, 'big') +   # lea TABLE,a1
    bytes.fromhex('12311000') +    # move.b (0,a1,d1.w),d1       map the other fighter's ID
    bytes.fromhex('4cdf0200') +    # movem.l (a7)+,a1
    bytes.fromhex('3e3c0003') +    # move.w #3,d7                (displaced)
    RTS)


def map_intro_opponent(data):
    result = bytearray(data)
    table = result[PRESENTATION_TABLE:PRESENTATION_TABLE + 64]
    if (table[:FIRST_UNUSED_ID] != bytes(range(FIRST_UNUSED_ID)) or
            table[IMPORTED_ID] >= FIRST_UNUSED_ID or table[IMPORTED_ID] == IMPORTED_ID):
        raise ValueError('presentation map is missing; run wire_slot_lookups.py first')
    if result[SITE:SITE + len(SITE_BYTES)] != SITE_BYTES:
        raise ValueError(f'unexpected intro opponent read at 0x{SITE:X}')
    if len(TRAMPOLINE_CODE) > TRAMPOLINE_END - TRAMPOLINE:
        raise ValueError('intro opponent routine does not fit')
    if result[TRAMPOLINE:TRAMPOLINE_END] != b'\xff' * (TRAMPOLINE_END - TRAMPOLINE):
        raise ValueError(f'intro opponent routine area 0x{TRAMPOLINE:X} is not empty')
    result[TRAMPOLINE:TRAMPOLINE + len(TRAMPOLINE_CODE)] = TRAMPOLINE_CODE
    result[SITE:SITE + len(SITE_BYTES)] = JSR_ABS + TRAMPOLINE.to_bytes(4, 'big') + NOP
    return result


def prepare(source, destination, expected_hash):
    private = PRIVATE.resolve(strict=True)
    source, destination = source.resolve(strict=True), destination.resolve()
    if not source.is_relative_to(private) or not destination.is_relative_to(private):
        raise ValueError('input and output must be inside private/')
    data = source.read_bytes()
    if len(data) != PROGRAM_SIZE or hashlib.sha256(data).hexdigest() != expected_hash.lower():
        raise ValueError('program size or SHA-256 does not match the supplied identity')
    result = map_intro_opponent(data)
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
        print(f'Cannot map the intro opponent: {error}', file=sys.stderr)
        return 1
    print(f'Mapped the intro opponent ID; SHA-256 {digest}.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
