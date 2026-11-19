"""Map the winner team's fighter IDs on the victory screen through the presentation map.

Run after wire_slot_lookups.py. It writes a new private program image; the input
is never changed. The victory screen copies the winning team's three bytes
(colour bits in 7-6, fighter ID in 5-0) from the match team list into its own
object before it picks the winner sprite, the win quote and the name plate. Those
lookups only know the original roster, so an imported ID such as $30 read past the
end of their tables. One six-byte call site is rerouted to a short routine that
keeps the colour bits and maps the ID through the 64-entry presentation map, so the
imported fighter wins as its source fighter.

It does not add art, palettes or quotes of its own for the imported fighter.
"""
import argparse
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PRIVATE = ROOT / 'private'
PROGRAM_SIZE = 0x900000
PRESENTATION_ROUTINE = 0x53140
PRESENTATION_TABLE = 0x53100
# Same routine wire_slot_lookups.py writes: save a0, d0 = table[d0], restore a0, return.
PRESENTATION_ROUTINE_BYTES = (b'\x2f\x08\x41\xf9' + PRESENTATION_TABLE.to_bytes(4, 'big') +
                              b'\x10\x30\x00\x00\x20\x5f\x4e\x75')
# Victory screen: copy of the winning team's three bytes, one per loop pass.
SITE = 0xE202
SITE_BYTES = bytes.fromhex('12f010005241')  # move.b (a0,d1.w),(a1)+ ; addq.w #1,d1
JSR_ABS = b'\x4e\xb9'
# Free fixed space right after the presentation map's area ($53100-$531FF).
TRAMPOLINE = 0x53200
TRAMPOLINE_END = 0x53240
TRAMPOLINE_CODE = (
    bytes.fromhex('2f00') +        # move.l d0,-(a7)
    bytes.fromhex('7000') +        # moveq #0,d0
    bytes.fromhex('10301000') +    # move.b (a0,d1.w),d0
    bytes.fromhex('3f00') +        # move.w d0,-(a7)
    bytes.fromhex('025700c0') +    # andi.w #$c0,(a7)        keep the colour bits
    bytes.fromhex('0240003f') +    # andi.w #$3f,d0          the fighter ID
    JSR_ABS + PRESENTATION_ROUTINE.to_bytes(4, 'big') +  # d0 = presentation ID
    bytes.fromhex('805f') +        # or.w (a7)+,d0
    bytes.fromhex('12c0') +        # move.b d0,(a1)+
    bytes.fromhex('201f') +        # move.l (a7)+,d0
    bytes.fromhex('5241') +        # addq.w #1,d1
    b'\x4e\x75')                   # rts


def map_victory_screen(data):
    result = bytearray(data)
    if result[PRESENTATION_ROUTINE:PRESENTATION_ROUTINE + 16] != PRESENTATION_ROUTINE_BYTES:
        raise ValueError('presentation map routine is missing; run wire_slot_lookups.py first')
    if result[SITE:SITE + len(SITE_BYTES)] != SITE_BYTES:
        raise ValueError(f'unexpected victory-screen team copy at 0x{SITE:X}')
    if len(TRAMPOLINE_CODE) > TRAMPOLINE_END - TRAMPOLINE:
        raise ValueError('victory-screen routine does not fit')
    if result[TRAMPOLINE:TRAMPOLINE_END] != b'\xff' * (TRAMPOLINE_END - TRAMPOLINE):
        raise ValueError(f'victory-screen routine area 0x{TRAMPOLINE:X} is not empty')
    result[TRAMPOLINE:TRAMPOLINE + len(TRAMPOLINE_CODE)] = TRAMPOLINE_CODE
    result[SITE:SITE + 6] = JSR_ABS + TRAMPOLINE.to_bytes(4, 'big')
    return result


def prepare(source, destination, expected_hash):
    private = PRIVATE.resolve(strict=True)
    source, destination = source.resolve(strict=True), destination.resolve()
    if not source.is_relative_to(private) or not destination.is_relative_to(private):
        raise ValueError('input and output must be inside private/')
    data = source.read_bytes()
    if len(data) != PROGRAM_SIZE or hashlib.sha256(data).hexdigest() != expected_hash.lower():
        raise ValueError('program size or SHA-256 does not match the supplied identity')
    result = map_victory_screen(data)
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
        print(f'Cannot map the victory screen: {error}', file=sys.stderr)
        return 1
    print(f'Mapped victory-screen fighter IDs; SHA-256 {digest}.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
