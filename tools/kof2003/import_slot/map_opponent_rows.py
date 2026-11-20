"""Install a separate combat proxy for the two 42-byte per-opponent row readers.

Accepts the validated original readers or the old private diagnostic patch.
Run after the slot-directory tools; rebuild native code after preparing the image.
Original IDs are identity-mapped; unassigned IDs use Kyo until configured. The
required --proxy selects the original row used for the rehearsal ID $30, without
changing its presentation, rival-intro or fighter-routine identity.
"""
import argparse
import hashlib
import sys
from pathlib import Path


PRIVATE = Path(__file__).resolve().parents[3] / 'private'
PROGRAM_SIZE = 0x900000
SITES = (0x216AC, 0x21836)
TABLE = 0x532C0
ROUTINE, ROUTINE_END = 0x53300, 0x53340
DIAGNOSTIC, DIAGNOSTIC_END = 0x52E00, 0x52E12
FIRST_UNUSED_ID, IMPORTED_ID, ENTRIES = 0x25, 0x30, 64
KYO = 0x1E  # default row for imported IDs that have not chosen a proxy yet
ROW_SIZE = 42
# The eight bytes of each reader (the load of the other fighter's ID and the multiply,
# the same two instructions the new routine repeats) and the old private diagnostic
# routine are checked by fingerprint; `moveq #0,d0` before each site is checked as is,
# as in map_fighter_handlers.py.
ORIGINAL_SITE_SHA256 = 'a1566e109e8af82167b89db2347e02c79ad8f83956b70b8a263dded0ac44a89b'
DIAGNOSTIC_SHA256 = 'da5a85049db1c4ec2849154e7784581bbdd5d8426596644011b1d69d415c6aae'
JSR, NOP = b'\x4e\xb9', b'\x4e\x71'
# New, hand-assembled routine: d0 was cleared by the checked caller. Preserve a0;
# read the opponent ID, map it, then return the 42-byte row offset in d0.
CODE = (bytes.fromhex('102b001f') +             # move.b (31,a3),d0
        bytes.fromhex('2f08') +                 # move.l a0,-(sp)
        bytes.fromhex('41f9') + TABLE.to_bytes(4, 'big') +  # lea TABLE,a0
        bytes.fromhex('10300000') +             # move.b (a0,d0.w),d0
        bytes.fromhex('205f') +                 # movea.l (sp)+,a0
        bytes.fromhex('c0fc') + ROW_SIZE.to_bytes(2, 'big') +  # mulu.w #42,d0
        bytes.fromhex('4e75'))                  # rts


def map_opponent_rows(data, proxy):
    if len(data) != PROGRAM_SIZE:
        raise ValueError('unexpected program size')
    if not 0 <= proxy < FIRST_UNUSED_ID:
        raise ValueError('proxy must name an original fighter (0x00 through 0x24)')
    diagnostic_call = JSR + DIAGNOSTIC.to_bytes(4, 'big') + NOP
    sites = [data[s:s + 8] for s in SITES]
    diagnostic = all(code == diagnostic_call for code in sites)
    original = all(hashlib.sha256(code).hexdigest() == ORIGINAL_SITE_SHA256 for code in sites)
    if not (diagnostic or original) or any(data[s - 2:s] != b'\x70\x00' for s in SITES):
        raise ValueError('unexpected opponent row reader code')
    old = data[DIAGNOSTIC:DIAGNOSTIC_END]
    if diagnostic:
        if hashlib.sha256(old).hexdigest() != DIAGNOSTIC_SHA256:
            raise ValueError('unexpected diagnostic routine')
    elif old != b'\xff' * len(old):
        raise ValueError('diagnostic area is not empty')
    if len(CODE) > ROUTINE_END - ROUTINE:
        raise ValueError('opponent proxy routine does not fit')
    if data[TABLE:ROUTINE_END] != b'\xff' * (ROUTINE_END - TABLE):
        raise ValueError('opponent proxy area is not empty')
    result = bytearray(data)
    table = bytearray(range(FIRST_UNUSED_ID)) + bytearray([KYO] * (ENTRIES - FIRST_UNUSED_ID))
    table[IMPORTED_ID] = proxy
    result[TABLE:TABLE + ENTRIES] = table
    result[ROUTINE:ROUTINE + len(CODE)] = CODE
    result[DIAGNOSTIC:DIAGNOSTIC_END] = b'\xff' * len(old)
    for site in SITES:
        result[site:site + 8] = JSR + ROUTINE.to_bytes(4, 'big') + NOP
    return result


def prepare(source, destination, expected_hash, proxy):
    private = PRIVATE.resolve(strict=True)
    source, destination = source.resolve(strict=True), destination.resolve()
    if not source.is_relative_to(private) or not destination.is_relative_to(private):
        raise ValueError('input and output must be inside private/')
    data = source.read_bytes()
    if len(data) != PROGRAM_SIZE or hashlib.sha256(data).hexdigest() != expected_hash.lower():
        raise ValueError('program size or SHA-256 does not match the supplied identity')
    result = map_opponent_rows(data, proxy)
    with destination.open('xb') as output:
        output.write(result)
    return hashlib.sha256(result).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--sha256', required=True)
    parser.add_argument('--proxy', required=True, type=lambda value: int(value, 0),
                        help='original fighter whose opponent row is used for ID 0x30')
    args = parser.parse_args()
    try:
        digest = prepare(args.source, args.destination, args.sha256, args.proxy)
    except (OSError, ValueError) as error:
        print(f'Cannot map opponent rows: {error}', file=sys.stderr)
        return 1
    print(f'Mapped opponent rows; SHA-256 {digest}.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
