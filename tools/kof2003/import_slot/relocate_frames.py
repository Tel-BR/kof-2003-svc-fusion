"""Copy one fighter's frame directory and redirect its tiles to Added Space.

The matching graphics copy and a 128 MiB descriptor are still required.
"""
import argparse
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PRIVATE = ROOT / 'private'
BANK = 0x200000
NEW_DIRECTORY = 0x2FB000
PROGRAM_SIZE = 0x900000
IMPORTED_ID = 0x30


def read_word(data, offset):
    return int.from_bytes(data[offset:offset + 2], 'big')


def read_long(data, offset):
    return int.from_bytes(data[offset:offset + 4], 'big')


def move_frame(data, start, limit):
    if start + 4 > limit:
        raise ValueError('truncated frame header')
    fmt, columns, rows = data[start + 1:start + 4]
    if fmt > 10 or (fmt in (0, 5, 7, 9) and rows > 16) or (fmt in (1, 6, 8, 10) and rows > 8):
        raise ValueError('unsupported frame format or row count')
    if not columns or not rows:
        return
    cursor = start + 4

    def require(length):
        if cursor + length > limit:
            raise ValueError('truncated frame body')

    def raise_attribute(offset):
        if data[offset] & 0x80:
            raise ValueError('frame already refers to Added Space')
        data[offset] |= 0x80

    if fmt in (0, 1):
        require(4 + columns * (2 if fmt == 0 else 1))
        if data[cursor + 1] & 8:
            raise ValueError('frame already refers to Added Space')
        data[cursor + 1] |= 8
        return

    if fmt in (3, 4, 7, 8, 9, 10):
        require(2)
        raise_attribute(cursor + 1)
        cursor += 2

    if fmt in (0, 5, 7, 9):
        require(columns * 2)
        masks = [read_word(data, cursor + 2 * c) for c in range(columns)]
        cursor += columns * 2
        drawn = sum(bool(mask & (0x8000 >> r)) for mask in masks for r in range(rows))
    elif fmt in (6, 8, 10):
        mask_length = columns if fmt == 10 else (columns + 1) & ~1
        require(mask_length)
        masks = data[cursor:cursor + columns]
        cursor += mask_length
        drawn = sum(bool(mask & (0x80 >> r)) for mask in masks for r in range(rows))
    else:
        drawn = columns * rows

    if fmt in (2, 5, 6):
        require(drawn * 3)
        for index in range(drawn):
            raise_attribute(cursor + 3 * index + (2 if index % 2 == 0 else 0))
    elif fmt in (3, 7, 8):
        require(drawn * 2)
    else:
        require(drawn)


def prepare(source, destination, expected_hash, fighter_id):
    private = PRIVATE.resolve(strict=True)
    source, destination = source.resolve(strict=True), destination.resolve()
    if not source.is_relative_to(private) or not destination.is_relative_to(private):
        raise ValueError('input and output must be inside private/')
    if not 0 <= fighter_id < 36:
        raise ValueError('fighter ID must have a following original directory')
    data = source.read_bytes()
    if len(data) != PROGRAM_SIZE or hashlib.sha256(data).hexdigest() != expected_hash.lower():
        raise ValueError('program size or SHA-256 does not match the supplied identity')
    relative = read_long(data, BANK + 4 * fighter_id)
    following = read_long(data, BANK + 4 * (fighter_id + 1))
    if read_long(data, BANK + 4 * IMPORTED_ID) != relative:
        raise ValueError('the imported directory does not point to the chosen fighter')
    start, end = BANK + relative, BANK + following
    if not BANK + 256 <= start < end <= NEW_DIRECTORY or end - start > 0x20000:
        raise ValueError('unexpected frame directory bounds')
    length = end - start
    if data[NEW_DIRECTORY:NEW_DIRECTORY + length] != b'\xff' * length:
        raise ValueError('destination directory space is not empty')
    count = read_word(data, start)
    if not 0 < count <= 1024 or start + 2 * count > end:
        raise ValueError('invalid frame count')
    offsets = [2 * read_word(data, start + 2 * index) for index in range(count)]
    if any(offset < count * 2 or start + offset + 4 > end for offset in offsets):
        raise ValueError('frame offset outside directory')
    result = bytearray(data)
    result[NEW_DIRECTORY:NEW_DIRECTORY + length] = data[start:end]
    unique = sorted(set(offsets))
    for index, offset in enumerate(unique):
        limit = NEW_DIRECTORY + (unique[index + 1] if index + 1 < len(unique) else length)
        move_frame(result, NEW_DIRECTORY + offset, limit)
    result[BANK + 4 * IMPORTED_ID:BANK + 4 * IMPORTED_ID + 4] = (NEW_DIRECTORY - BANK).to_bytes(4, 'big')
    with destination.open('xb') as output:
        output.write(result)
    return count, hashlib.sha256(result).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--sha256', required=True)
    parser.add_argument('--fighter-id', required=True, type=lambda value: int(value, 0))
    args = parser.parse_args()
    try:
        count, digest = prepare(args.source, args.destination, args.sha256, args.fighter_id)
    except (OSError, ValueError) as error:
        print(f'Cannot relocate frames: {error}', file=sys.stderr)
        return 1
    print(f'Copied {count} frame references; SHA-256 {digest}. Graphics copy still required.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
