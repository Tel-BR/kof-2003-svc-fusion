"""Give the imported ID $30 its source fighter's hit-box kind set.

The collision routine reads, at $15D08 and $169CA, a 64-entry table of pointers at
$6C62E by the box owner's ID (4 * (ID & $3F)); each pointer leads to a 16-byte bit
set of hit-box kinds. Entries $25-$3F share one pointer, fighter $24's set, so an
imported ID classified its boxes with that set. This step copies the source
fighter's pointer to entry $30 (data only: no code changes, no native rebuild).

Run after map_opponent_rows.py. It writes a new private image; the input is never
changed. It checks that the unused entries still share fighter $24's set, that $30
has no own entry yet, that the source fighter has its own set and that every
original set lies in the fixed program area ($000000-$0FFFFF) and off the table.
"""
import argparse
import hashlib
import sys
from pathlib import Path


PRIVATE = Path(__file__).resolve().parents[3] / 'private'
PROGRAM_SIZE = 0x900000
FIXED_END = 0x100000  # sets are read from the fixed 1 MiB, never from the banked window
TABLE = 0x6C62E
ENTRIES, ENTRY_SIZE, SET_SIZE = 64, 4, 16
FIRST_UNUSED_ID, IMPORTED_ID = 0x25, 0x30


def pointer(data, fighter):
    start = TABLE + ENTRY_SIZE * fighter
    return int.from_bytes(data[start:start + ENTRY_SIZE], 'big')


def map_hitbox_kinds(data, fighter_id):
    if len(data) != PROGRAM_SIZE:
        raise ValueError('unexpected program size')
    if not 0 <= fighter_id < FIRST_UNUSED_ID:
        raise ValueError('fighter ID must name an original fighter (0x00 through 0x24)')
    default = pointer(data, FIRST_UNUSED_ID - 1)
    unused = [i for i in range(FIRST_UNUSED_ID, ENTRIES) if i != IMPORTED_ID]
    if any(pointer(data, i) != default for i in unused):
        raise ValueError(f'table 0x{TABLE:X} has no shared default (fighter $24\'s set) above $24')
    if pointer(data, IMPORTED_ID) != default:
        raise ValueError(f'entry ${IMPORTED_ID:02X} of table 0x{TABLE:X} already has its own set')
    if pointer(data, fighter_id) == default:
        raise ValueError(f'fighter 0x{fighter_id:02X} has no own set in table 0x{TABLE:X}')
    for fighter in range(FIRST_UNUSED_ID):
        target = pointer(data, fighter)
        if target + SET_SIZE > FIXED_END:
            raise ValueError(f'set of fighter 0x{fighter:02X} lies outside the fixed program area')
        if TABLE - SET_SIZE < target < TABLE + ENTRIES * ENTRY_SIZE:
            raise ValueError(f'set of fighter 0x{fighter:02X} lies on the table')
    result = bytearray(data)
    start = TABLE + ENTRY_SIZE * IMPORTED_ID
    result[start:start + ENTRY_SIZE] = pointer(data, fighter_id).to_bytes(ENTRY_SIZE, 'big')
    return result


def prepare(source, destination, expected_hash, fighter_id):
    private = PRIVATE.resolve(strict=True)
    source, destination = source.resolve(strict=True), destination.resolve()
    if not source.is_relative_to(private) or not destination.is_relative_to(private):
        raise ValueError('input and output must be inside private/')
    data = source.read_bytes()
    if len(data) != PROGRAM_SIZE or hashlib.sha256(data).hexdigest() != expected_hash.lower():
        raise ValueError('program size or SHA-256 does not match the supplied identity')
    result = map_hitbox_kinds(data, fighter_id)
    with destination.open('xb') as output:
        output.write(result)
    return hashlib.sha256(result).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--sha256', required=True, help='expected SHA-256 of the input')
    parser.add_argument('--fighter-id', required=True, type=lambda value: int(value, 0),
                        help=f'original fighter whose hit-box kind set ID 0x{IMPORTED_ID:02X} uses')
    args = parser.parse_args()
    try:
        digest = prepare(args.source, args.destination, args.sha256, args.fighter_id)
    except (OSError, ValueError) as error:
        print(f'Cannot map hit-box kinds: {error}', file=sys.stderr)
        return 1
    print(f'Mapped hit-box kind set of ${IMPORTED_ID:02X}; SHA-256 {digest}.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
