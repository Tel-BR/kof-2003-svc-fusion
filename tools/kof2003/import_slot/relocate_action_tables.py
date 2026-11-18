"""Prepare expanded fighter tables in a new private program image.

This is one intermediate step, not a playable build. The input remains untouched.
"""
import argparse
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PRIVATE = ROOT / 'private'
TABLES = (
    (0x706A2, 0x166C0), (0x70FE2, 0x28C38), (0x71922, 0x28C46),
    (0x72262, 0x28C54), (0x72BA2, 0x28C62), (0x734E2, 0x28C70),
    (0x73E22, 0x28C7E), (0x74762, 0x28C8C), (0x75C22, 0x28C9A),
)
DESTINATION = 0x44020
SMALL_TABLES = ((0x77A22, (0x24138, 0x27E1A)),
                (0x77AB6, (0x24156, 0x27E38)),
                (0xA5F56, (0x3C6E4,)), (0xA5FEA, (0x3C6F6,)),
                (0xAAFD4, (0x234F0, 0x3C7F0)), (0xB2280, (0x235B0,)))
ROW_SIZE = 64
ROWS = 64
IMPORTED_ID = 0x30
PROGRAM_SIZE = 0x900000
WIDE_TABLE, WIDE_REFERENCE = 0x750A2, 0x28CBC
WIDE_ROW_SIZE = 80
MATRIX = 0x77B4A
MATRIX_REFERENCES = (0x240E6, 0x24D06)
MATRIX_STRIDES = (0x24100, 0x24D0E)
OLD_MATRIX_STRIDE = 37 * 4
NEW_MATRIX_STRIDE = ROWS * 4
DIRECTORIES = ((0x704A2, 4), (0x6090A, 2), (0x6098A, 2),
               (0x60A0A, 2), (0x60A8A, 2), (0x7DC28, 2),
               (0x200000, 4), (0x380000, 4))


def prepare(source, destination, expected_hash, fighter_id):
    private = PRIVATE.resolve(strict=True)
    source = source.resolve(strict=True)
    destination = destination.resolve()
    if not source.is_relative_to(private) or not destination.is_relative_to(private):
        raise ValueError('input and output must be inside private/')
    if not 0 <= fighter_id < 37:
        raise ValueError('fighter ID must be an original ID from 0 to 36')
    data = source.read_bytes()
    if len(data) != PROGRAM_SIZE or hashlib.sha256(data).hexdigest() != expected_hash.lower():
        raise ValueError('program size or SHA-256 does not match the supplied identity')
    size = (len(TABLES) * ROW_SIZE * ROWS + len(SMALL_TABLES) * 4 * ROWS
            + WIDE_ROW_SIZE * ROWS + NEW_MATRIX_STRIDE * ROWS)
    if data[DESTINATION:DESTINATION + size] != b'\xff' * size:
        raise ValueError('relocation space is not empty')
    for table, reference in TABLES:
        if int.from_bytes(data[reference:reference + 4], 'big') != table:
            raise ValueError(f'unexpected table reference at 0x{reference:X}')
    for table, references in SMALL_TABLES:
        for reference in references:
            if int.from_bytes(data[reference:reference + 4], 'big') != table:
                raise ValueError(f'unexpected table reference at 0x{reference:X}')
    if int.from_bytes(data[WIDE_REFERENCE:WIDE_REFERENCE + 4], 'big') != WIDE_TABLE:
        raise ValueError(f'unexpected table reference at 0x{WIDE_REFERENCE:X}')
    for reference in MATRIX_REFERENCES:
        if int.from_bytes(data[reference:reference + 4], 'big') != MATRIX:
            raise ValueError(f'unexpected matrix reference at 0x{reference:X}')
    for immediate in MATRIX_STRIDES:
        if int.from_bytes(data[immediate:immediate + 2], 'big') != OLD_MATRIX_STRIDE:
            raise ValueError(f'unexpected matrix stride at 0x{immediate:X}')
    result = bytearray(data)
    for index, (table, reference) in enumerate(TABLES):
        relocated = DESTINATION + index * ROW_SIZE * ROWS
        # Preserve the old indexed reads, even those beyond the original 37 rows.
        result[relocated:relocated + ROW_SIZE * ROWS] = data[table:table + ROW_SIZE * ROWS]
        start = table + fighter_id * ROW_SIZE
        target = relocated + IMPORTED_ID * ROW_SIZE
        result[target:target + ROW_SIZE] = data[start:start + ROW_SIZE]
        result[reference:reference + 4] = relocated.to_bytes(4, 'big')
    base = DESTINATION + len(TABLES) * ROW_SIZE * ROWS
    for index, (table, references) in enumerate(SMALL_TABLES):
        relocated = base + index * 4 * ROWS
        result[relocated:relocated + 4 * ROWS] = data[table:table + 4 * ROWS]
        target = relocated + IMPORTED_ID * 4
        result[target:target + 4] = data[table + fighter_id * 4:table + fighter_id * 4 + 4]
        for reference in references:
            result[reference:reference + 4] = relocated.to_bytes(4, 'big')
    relocated = base + len(SMALL_TABLES) * 4 * ROWS
    result[relocated:relocated + WIDE_ROW_SIZE * ROWS] = data[
        WIDE_TABLE:WIDE_TABLE + WIDE_ROW_SIZE * ROWS]
    target = relocated + IMPORTED_ID * WIDE_ROW_SIZE
    start = WIDE_TABLE + fighter_id * WIDE_ROW_SIZE
    result[target:target + WIDE_ROW_SIZE] = data[start:start + WIDE_ROW_SIZE]
    result[WIDE_REFERENCE:WIDE_REFERENCE + 4] = relocated.to_bytes(4, 'big')
    matrix = relocated + WIDE_ROW_SIZE * ROWS
    for row in range(ROWS):
        source_row = fighter_id if row == IMPORTED_ID else row
        for column in range(ROWS):
            source_column = fighter_id if column == IMPORTED_ID else column
            start = MATRIX + source_row * OLD_MATRIX_STRIDE + source_column * 4
            target = matrix + row * NEW_MATRIX_STRIDE + column * 4
            result[target:target + 4] = data[start:start + 4]
    for reference in MATRIX_REFERENCES:
        result[reference:reference + 4] = matrix.to_bytes(4, 'big')
    for immediate in MATRIX_STRIDES:
        result[immediate:immediate + 2] = NEW_MATRIX_STRIDE.to_bytes(2, 'big')
    for base, width in DIRECTORIES:
        start = base + fighter_id * width
        target = base + IMPORTED_ID * width
        result[target:target + width] = data[start:start + width]
    with destination.open('xb') as output:
        output.write(result)
    return hashlib.sha256(result).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--sha256', required=True, help='expected SHA-256 of the input')
    parser.add_argument('--fighter-id', required=True, type=lambda value: int(value, 0))
    args = parser.parse_args()
    try:
        digest = prepare(args.source, args.destination, args.sha256, args.fighter_id)
    except (OSError, ValueError) as error:
        print(f'Cannot prepare tables: {error}', file=sys.stderr)
        return 1
    print(f'Prepared intermediate image; SHA-256 {digest}. It is not playable yet.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
