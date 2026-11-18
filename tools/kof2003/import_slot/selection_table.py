"""Prepare provisional imported cells in a new private program image.

This intermediate image still needs the ID guards and presentation work.
"""
import argparse
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PRIVATE = ROOT / 'private'
PROGRAM_SIZE = 0x900000
OLD_TABLE = 0x9856
NEW_TABLE = 0x52A20
HELPER = 0x52B40
OLD_CELLS = 39
NEW_CELLS = 45


def word(data, offset):
    return int.from_bytes(data[offset:offset + 2], 'big')


def signed_word(data, offset):
    return int.from_bytes(data[offset:offset + 2], 'big', signed=True)


def prepare(source, destination, expected_hash):
    private = PRIVATE.resolve(strict=True)
    source, destination = source.resolve(strict=True), destination.resolve()
    if not source.is_relative_to(private) or not destination.is_relative_to(private):
        raise ValueError('input and output must be inside private/')
    data = source.read_bytes()
    if len(data) != PROGRAM_SIZE or hashlib.sha256(data).hexdigest() != expected_hash.lower():
        raise ValueError('program size or SHA-256 does not match the supplied identity')
    if data[NEW_TABLE:HELPER + 32] != b'\xff' * (HELPER + 32 - NEW_TABLE):
        raise ValueError('selection table or helper space is not empty')
    if (data[0x9523] != 10 or word(data, 0x9556) != 10
            or word(data, 0x95DA) != 38 or data[0x95E1] != 38
            or 0x9600 + signed_word(data, 0x9600) != OLD_TABLE):
        raise ValueError('selection code differs from the expected layout')
    result = bytearray(data)
    result[NEW_TABLE:NEW_TABLE + OLD_CELLS * 6] = data[OLD_TABLE:OLD_TABLE + OLD_CELLS * 6]
    for index in range(6):
        column, extra_row = index % 3, index // 3 + 1
        previous = OLD_TABLE + (11 * 3 + column) * 6
        last = OLD_TABLE + (12 * 3 + column) * 6
        y = signed_word(data, last + 2) + extra_row * (signed_word(data, last + 2) - signed_word(data, previous + 2))
        if not -32768 <= y <= 32767:
            raise ValueError('new selection coordinate is out of range')
        cell = NEW_TABLE + (OLD_CELLS + index) * 6
        result[cell:cell + 2] = data[last:last + 2]
        result[cell + 2:cell + 4] = y.to_bytes(2, 'big', signed=True)
        result[cell + 4:cell + 6] = (0x30 if index == 0 else 0xFFFF).to_bytes(2, 'big')
    # A small new 68000 helper loads the relocated table, executes the original
    # non-PC-relative cell-coordinate instruction and jumps back to selection.
    helper = (0x47F9).to_bytes(2, 'big') + NEW_TABLE.to_bytes(4, 'big')
    helper += data[0x9602:0x9608]
    helper += (0x4EF9).to_bytes(2, 'big') + (0x9608).to_bytes(4, 'big')
    result[HELPER:HELPER + len(helper)] = helper
    result[0x95FE:0x9608] = ((0x4EF9).to_bytes(2, 'big') + HELPER.to_bytes(4, 'big')
                             + (0x4E71).to_bytes(2, 'big') * 2)
    result[0x9523] = 14
    result[0x952A] = 0x60
    result[0x9556:0x9558] = (14).to_bytes(2, 'big')
    result[0x95DA:0x95DC] = (NEW_CELLS - 1).to_bytes(2, 'big')
    result[0x95E1] = NEW_CELLS - 1
    with destination.open('xb') as output:
        output.write(result)
    return hashlib.sha256(result).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--sha256', required=True)
    args = parser.parse_args()
    try:
        digest = prepare(args.source, args.destination, args.sha256)
    except (OSError, ValueError) as error:
        print(f'Cannot prepare selection: {error}', file=sys.stderr)
        return 1
    print(f'Prepared provisional selection cells; SHA-256 {digest}. Not yet playable.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
