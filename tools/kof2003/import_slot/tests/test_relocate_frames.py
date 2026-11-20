"""Exercise frame relocation into a per-ID bank through the command with invented program data."""
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TOOL = ROOT / 'tools/kof2003/import_slot/relocate_frames.py'
sys.path.insert(0, str(TOOL.parent))
from relocate_frames import (AREA, AREA_END, BANK_ROUTINE, DIRECTORY_ROUTINE,  # noqa: E402
                             DIRECTORY_SITES, DRAW_ROUTINE, DRAW_SITES, LOOKUP_SITES,
                             ROUTINES, TABLE)

DESTINATION = 0x700000
FRAME = bytes.fromhex('0001 00010101 0001 1234 80 0000000000')
MOVED = bytes.fromhex('0001 00010101 0009 1234 80 0000000000')


def jsr(target):
    return b'\x4e\xb9' + target.to_bytes(4, 'big')


def invented_program(length=0x10):
    """Generic 68000 encodings around each site; the frame data is invented."""
    data = bytearray(0x900000)
    data[AREA:AREA_END] = b'\xff' * (AREA_END - AREA)
    data[0x300000:0x900000] = b'\xff' * 0x600000
    for index, offset in ((5, 0x10000), (6, 0x10000 + length), (0x30, 0x10000)):
        at = 0x200000 + index * 4
        data[at:at + 4] = offset.to_bytes(4, 'big')
    data[0x210000:0x210010] = FRAME
    for site in LOOKUP_SITES:
        data[site - 4:site] = bytes.fromhex('48e78100')              # movem.l d0/d7,-(a7)
        data[site:site + 6] = bytes.fromhex('203c00100000')          # move.l #$100000,d0
        data[site + 6:site + 12] = bytes.fromhex('23c0002ff000')     # move.l d0,$2ff000
    for site in DIRECTORY_SITES:
        data[site:site + 10] = bytes.fromhex('43f900200000d3f12000')  # lea $200000,a1; adda.l (a1,d2.w),a1
    for site in DRAW_SITES:
        data[site - 4:site] = bytes.fromhex('48e78100')
        data[site:site + 6] = bytes.fromhex('203c00100000')
        data[site + 6:site + 12] = bytes.fromhex('23c0002ff000')
        data[site + 0x40:site + 0x44] = bytes.fromhex('226d07a6')    # movea.l ($7a6,a5),a1
    return data


def run(data, temp, destination=DESTINATION, fighter='5', digest=None):
    source, output = Path(temp) / 'input.bin', Path(temp) / 'output.bin'
    source.write_bytes(data)
    result = subprocess.run([sys.executable, str(TOOL), str(source), str(output),
                             '--sha256', digest or hashlib.sha256(data).hexdigest(),
                             '--fighter-id', fighter, '--file-offset', hex(destination)],
                            capture_output=True, text=True)
    return result, source, output


def test_command_copies_frames_to_their_own_bank_and_installs_bank_selecting_readers():
    with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
        data = invented_program()
        result, source, output = run(data, temp)
        assert result.returncode == 0, result.stderr
        assert source.read_bytes() == data
        out = output.read_bytes()
        # The copy sits at the start of its own window; tiles move to Added Space.
        assert out[DESTINATION:DESTINATION + 0x10] == MOVED
        # The frame bank is untouched: the original directory and every entry stay.
        assert out[0x200000:0x300000] == data[0x200000:0x300000]
        # Per-ID bank values: the frame bank for every ID except $30.
        banks = [int.from_bytes(out[TABLE + 4 * i:TABLE + 4 * i + 4], 'big') for i in range(64)]
        assert banks[0x30] == DESTINATION - 0x100000
        assert all(bank == 0x100000 for i, bank in enumerate(banks) if i != 0x30)
        assert out[BANK_ROUTINE:BANK_ROUTINE + len(ROUTINES)] == ROUTINES
        for site in LOOKUP_SITES:
            assert out[site:site + 6] == jsr(BANK_ROUTINE)
        for site in DIRECTORY_SITES:
            assert out[site:site + 10] == jsr(DIRECTORY_ROUTINE) + b'\x4e\x71' * 2
        for site in DRAW_SITES:
            assert out[site:site + 6] == jsr(DRAW_ROUTINE)
        sites = [(s, 6) for s in LOOKUP_SITES + DRAW_SITES] + [(s, 10) for s in DIRECTORY_SITES]
        changed = (i for i, (a, b) in enumerate(zip(data, out)) if a != b)
        assert all(any(s <= i < s + n for s, n in sites) or AREA <= i < AREA_END or
                   DESTINATION <= i < DESTINATION + 0x10 for i in changed)
        assert 'SHA-256' in result.stdout


def test_command_refuses_unchecked_placements_without_writing():
    cases = (
        (0x2FB000, None, 'frame bank'),          # inside the frame bank, reaching the PVC window
        (0x2FF000, None, 'frame bank'),          # inside the PVC window
        (0x1F0000, None, 'frame bank'),          # below the frame bank: a fixed-area bank value
        (0x700001, None, 'even'),
        (0x8FFFF8, None, 'program'),
        (DESTINATION, (DESTINATION + 6, 0), 'not empty'),
    )
    for destination, poke, message in cases:
        with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
            data = invented_program()
            if poke:
                data[poke[0]] = poke[1]
            result, _, output = run(data, temp, destination=destination)
            assert result.returncode == 1, (hex(destination), result.stdout)
            assert message in result.stderr, (hex(destination), result.stderr)
            assert not output.exists()


def test_command_refuses_unexpected_reader_code_and_occupied_space():
    pokes = [(LOOKUP_SITES[1] + 2, 0x20, 'reader code'), (LOOKUP_SITES[2] - 1, 1, 'reader code'),
             (DIRECTORY_SITES[0] + 8, 0x30, 'reader code'), (DRAW_SITES[2] + 0x41, 1, 'reader code'),
             (DRAW_SITES[0] + 7, 1, 'reader code'), (TABLE + 0x100, 0, 'not empty'),
             (AREA_END - 1, 0, 'not empty'), (0x2000C0 + 3, 0x10, 'chosen fighter')]
    for address, value, message in pokes:
        with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
            data = invented_program()
            data[address] = value
            result, _, output = run(data, temp)
            assert result.returncode == 1, hex(address)
            assert message in result.stderr, (hex(address), result.stderr)
            assert not output.exists()


def test_command_refuses_paths_outside_private_and_wrong_identity():
    with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
        data = invented_program()
        result, _, output = run(data, temp, digest='0' * 64)
        assert result.returncode == 1 and 'SHA-256' in result.stderr
        assert not output.exists()
    with tempfile.TemporaryDirectory() as temp:
        result, _, output = run(invented_program(), temp)
        assert result.returncode == 1 and 'private/' in result.stderr
