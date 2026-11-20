"""Copy one fighter's frame directory into its own bank and make the frame readers select it.

All original frame directories live in one bank, and KOF 2003's NEO-PVC chip maps 8 KiB
of RAM over the top of that window ($2FE000-$2FFFFF), so there is no room left for an
imported fighter. By the owner's decision imported frame data lives in another bank
selected per ID. This step copies the chosen fighter's directory to unused banked space
outside the frame bank, at the start of its own window, and redirects its tiles to the
Added Space. It installs a 64-entry table of bank values (the frame bank for every ID
except $30) and three short routines:

* the three directory lookups ($010AF8-$010DA2) select the bank of the object's ID and,
  for an ID with its own bank, take the directory from the start of that window; the
  frame pointers they store (+$60, +$6E, +$7C) then carry that ID in their top byte,
  which the 68000's 24-bit address bus ignores;
* the three sprite layers of the drawer ($0F85D4, $0F8704, $0F8834) select the bank named
  by the top byte of the frame pointer they draw, so a pointer copied into another
  object still reads its own bank.

Original IDs keep the frame bank and untagged pointers. The input is never changed;
rebuild native code after preparing the image (the readers change). The matching
graphics copy and a 128 MiB descriptor are still required.
"""
import argparse
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PRIVATE = ROOT / 'private'
PROGRAM_SIZE = 0x900000
IMPORTED_ID = 0x30
ENTRIES = 64
# The frame directory table and every original directory are in the bank that starts at
# this file offset; the game selects it with this bank value (file offset - $100000).
BANK = 0x200000
FRAME_BANK_VALUE = 0x100000
# The NEO-PVC chip maps 8 KiB of RAM over $2FE000-$2FFFFF of the window, whatever the bank,
# so only $FE000 bytes of a window read back as program data.
PVC_WINDOW = 0x2FE000
WINDOW_DATA = PVC_WINDOW - 0x200000
FRAME_BANK_END = BANK + 0x100000
# Bank values below $100000 mean "fixed area" to the game's pointer conversions, so an own
# bank must start after the frame bank.
# Free fixed space after the opponent proxy routine ($53300-$5333F).
AREA, AREA_END = 0x53340, 0x53500
TABLE = AREA
BANK_ROUTINE = TABLE + 4 * ENTRIES

# Original instructions at the sites (generic 68000 encodings).
MOVEM_SAVE = bytes.fromhex('48e78100')                  # movem.l d0/d7,-(a7)
MOVE_FRAME_BANK = bytes.fromhex('203c00100000')         # move.l #$100000,d0
STORE_BANK = bytes.fromhex('23c0002ff000')              # move.l d0,$2ff000
DIRECTORY_CODE = bytes.fromhex('43f900200000d3f12000')  # lea $200000,a1 ; adda.l (a1,d2.w),a1
LOAD_DRAWN_FRAME = bytes.fromhex('226d07a6')            # movea.l ($7a6,a5),a1
LOOKUP_SITES = (0x10AB8, 0x10BF8, 0x10D26)
DIRECTORY_SITES = (0x10B0A, 0x10C38, 0x10D66)
DRAW_SITES = (0xF85D4, 0xF8704, 0xF8834)
DRAW_LOAD_DISTANCE = 0x40   # from each drawer's bank value to its load of the drawn frame
JSR, NOP = b'\x4e\xb9', b'\x4e\x71'


def _long(value):
    return value.to_bytes(4, 'big')


# New, hand-assembled routines.
# Bank of the object at a4: d0 = TABLE[ID], with the lookup's own clamp of IDs above $3F.
BANK_CODE = (bytes.fromhex('302c001e') +        # move.w ($1e,a4),d0
             bytes.fromhex('0c40003f') +        # cmpi.w #$3f,d0
             bytes.fromhex('6302') +            # bls.s +2
             bytes.fromhex('7000') +            # moveq #0,d0
             bytes.fromhex('d040d040') +        # add.w d0,d0 ; add.w d0,d0
             bytes.fromhex('2f09') +            # move.l a1,-(a7)
             bytes.fromhex('43f9') + _long(TABLE) +  # lea TABLE,a1
             bytes.fromhex('20310000') +        # move.l (a1,d0.w),d0
             bytes.fromhex('225f') +            # movea.l (a7)+,a1
             bytes.fromhex('4e75'))             # rts
DIRECTORY_ROUTINE = BANK_ROUTINE + len(BANK_CODE)
# Directory of the ID in d2 (4 * ID, as the lookup computed it): a1 = start of the directory.
# Frame-bank IDs repeat the displaced instructions; an own-bank ID's directory is at the
# start of its window and a1 carries the ID in its top byte. Every other register is kept.
DIRECTORY_CODE_NEW = (bytes.fromhex('2f00') +           # move.l d0,-(a7)
                      bytes.fromhex('43f9') + _long(TABLE) +  # lea TABLE,a1
                      bytes.fromhex('20312000') +       # move.l (a1,d2.w),d0
                      bytes.fromhex('0c80') + _long(FRAME_BANK_VALUE) +  # cmpi.l #$100000,d0
                      bytes.fromhex('660e') +           # bne.s own
                      DIRECTORY_CODE +                  # (displaced)
                      bytes.fromhex('201f') +           # move.l (a7)+,d0
                      bytes.fromhex('4e75') +           # rts
                      bytes.fromhex('7000') +           # own: moveq #0,d0
                      bytes.fromhex('3002') +           # move.w d2,d0
                      bytes.fromhex('ed48') +           # lsl.w #6,d0      (ID << 8)
                      bytes.fromhex('4840') +           # swap d0          (ID << 24)
                      bytes.fromhex('0680') + _long(0x200000) +  # addi.l #$200000,d0
                      bytes.fromhex('2240') +           # movea.l d0,a1
                      bytes.fromhex('201f') +           # move.l (a7)+,d0
                      bytes.fromhex('4e75'))            # rts
DRAW_ROUTINE = DIRECTORY_ROUTINE + len(DIRECTORY_CODE_NEW)
# Bank of the frame about to be drawn: d0 = TABLE[top byte of ($7a6,a5)]; untagged
# original pointers give entry 0, the frame bank.
DRAW_CODE = (bytes.fromhex('202d07a6') +        # move.l ($7a6,a5),d0
             bytes.fromhex('e198') +            # rol.l #8,d0
             bytes.fromhex('0240003f') +        # andi.w #$3f,d0
             bytes.fromhex('d040d040') +        # add.w d0,d0 ; add.w d0,d0
             bytes.fromhex('2f09') +            # move.l a1,-(a7)
             bytes.fromhex('43f9') + _long(TABLE) +  # lea TABLE,a1
             bytes.fromhex('20310000') +        # move.l (a1,d0.w),d0
             bytes.fromhex('225f') +            # movea.l (a7)+,a1
             bytes.fromhex('4e75'))             # rts
ROUTINES = BANK_CODE + DIRECTORY_CODE_NEW + DRAW_CODE


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


def check_readers(data):
    for site in LOOKUP_SITES + DRAW_SITES:
        if (data[site - 4:site] != MOVEM_SAVE or data[site:site + 6] != MOVE_FRAME_BANK or
                data[site + 6:site + 12] != STORE_BANK):
            raise ValueError(f'unexpected frame reader code at 0x{site:X}')
    for site in DRAW_SITES:
        load = site + DRAW_LOAD_DISTANCE
        if data[load:load + 4] != LOAD_DRAWN_FRAME:
            raise ValueError(f'unexpected frame reader code at 0x{load:X}')
    for site in DIRECTORY_SITES:
        if data[site:site + len(DIRECTORY_CODE)] != DIRECTORY_CODE:
            raise ValueError(f'unexpected frame reader code at 0x{site:X}')


def check_placement(data, destination, length):
    if destination % 2:
        raise ValueError('the bank must start at an even file offset')
    if destination < FRAME_BANK_END:
        raise ValueError('the copy must start after the frame bank and its NEO-PVC window '
                         f'(file offset 0x{FRAME_BANK_END:X} or later)')
    if length > WINDOW_DATA:
        raise ValueError('frame directory does not fit in one window below the NEO-PVC RAM')
    if destination + length > PROGRAM_SIZE:
        raise ValueError('the copy would run past the end of the program')
    if data[destination:destination + length] != b'\xff' * length:
        raise ValueError('destination space is not empty')


def place_frames(data, fighter_id, destination):
    if len(data) != PROGRAM_SIZE:
        raise ValueError('unexpected program size')
    if not 0 <= fighter_id < 36:
        raise ValueError('fighter ID must have a following original directory')
    relative = read_long(data, BANK + 4 * fighter_id)
    following = read_long(data, BANK + 4 * (fighter_id + 1))
    if read_long(data, BANK + 4 * IMPORTED_ID) != relative:
        raise ValueError('the imported directory does not point to the chosen fighter')
    start, end = BANK + relative, BANK + following
    if not BANK + 256 <= start < end <= PVC_WINDOW:
        raise ValueError('unexpected frame directory bounds')
    length = end - start
    check_placement(data, destination, length)
    count = read_word(data, start)
    if not 0 < count <= 1024 or start + 2 * count > end:
        raise ValueError('invalid frame count')
    offsets = [2 * read_word(data, start + 2 * index) for index in range(count)]
    if any(offset < count * 2 or start + offset + 4 > end for offset in offsets):
        raise ValueError('frame offset outside directory')
    check_readers(data)
    if data[AREA:AREA_END] != b'\xff' * (AREA_END - AREA):
        raise ValueError('frame bank table area is not empty')
    if len(ROUTINES) > AREA_END - BANK_ROUTINE:
        raise ValueError('frame bank routines do not fit')
    result = bytearray(data)
    result[destination:destination + length] = data[start:end]
    unique = sorted(set(offsets))
    for index, offset in enumerate(unique):
        limit = destination + (unique[index + 1] if index + 1 < len(unique) else length)
        move_frame(result, destination + offset, limit)
    banks = [FRAME_BANK_VALUE] * ENTRIES
    banks[IMPORTED_ID] = destination - 0x100000
    result[TABLE:TABLE + 4 * ENTRIES] = b''.join(_long(bank) for bank in banks)
    result[BANK_ROUTINE:BANK_ROUTINE + len(ROUTINES)] = ROUTINES
    for site in LOOKUP_SITES:
        result[site:site + 6] = JSR + _long(BANK_ROUTINE)
    for site in DIRECTORY_SITES:
        result[site:site + 10] = JSR + _long(DIRECTORY_ROUTINE) + NOP * 2
    for site in DRAW_SITES:
        result[site:site + 6] = JSR + _long(DRAW_ROUTINE)
    return count, result


def prepare(source, destination, expected_hash, fighter_id, file_offset):
    private = PRIVATE.resolve(strict=True)
    source, destination = source.resolve(strict=True), destination.resolve()
    if not source.is_relative_to(private) or not destination.is_relative_to(private):
        raise ValueError('input and output must be inside private/')
    data = source.read_bytes()
    if len(data) != PROGRAM_SIZE or hashlib.sha256(data).hexdigest() != expected_hash.lower():
        raise ValueError('program size or SHA-256 does not match the supplied identity')
    count, result = place_frames(data, fighter_id, file_offset)
    with destination.open('xb') as output:
        output.write(result)
    return count, hashlib.sha256(result).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--sha256', required=True)
    parser.add_argument('--fighter-id', required=True, type=lambda value: int(value, 0))
    parser.add_argument('--file-offset', required=True, type=lambda value: int(value, 0),
                        help='program file offset of the copy (start of the bank of ID 0x30)')
    args = parser.parse_args()
    try:
        count, digest = prepare(args.source, args.destination, args.sha256, args.fighter_id,
                                args.file_offset)
    except (OSError, ValueError) as error:
        print(f'Cannot relocate frames: {error}', file=sys.stderr)
        return 1
    print(f'Copied {count} frame references to the bank at 0x{args.file_offset:X}; '
          f'SHA-256 {digest}. Rebuild native code; graphics copy still required.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
