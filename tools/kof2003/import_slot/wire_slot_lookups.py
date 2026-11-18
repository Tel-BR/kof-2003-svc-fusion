"""Wire the remaining fighter-ID lookups of a relocated program image to ID $30.

Run after relocate_action_tables.py. It writes a new private image; the input
is never changed. Each change is checked against the expected bytes first:

* raise four ID guards that still stop at $24/$25 in front of tables that are
  already relocated to 64 rows;
* move the two 37-entry special-intro tables to 64 rows in unused fixed space,
  repoint their readers and copy the source fighter's entry to $30;
* copy the source fighter's entry to $30 in 64-entry lookup tables whose
  entries above $24 hold a shared default.

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


def word(data, offset):
    return int.from_bytes(data[offset:offset + 2], 'big')


def long(data, offset):
    return int.from_bytes(data[offset:offset + 4], 'big')


def wire(data, fighter_id):
    result = bytearray(data)
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
