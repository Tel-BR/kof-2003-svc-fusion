"""Test the hit-box kind set step using an invented program image."""
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TOOL = ROOT / 'tools/kof2003/import_slot/map_hitbox_kinds.py'
TABLE = 0x6C62E
SETS = 0x6C72E  # invented 16-byte sets right after the 64 pointers
IMPORTED_ENTRY = TABLE + 4 * 0x30


def pointer(data, fighter):
    return int.from_bytes(data[TABLE + 4 * fighter:TABLE + 4 * fighter + 4], 'big')


def set_pointer(data, fighter, target):
    data[TABLE + 4 * fighter:TABLE + 4 * fighter + 4] = target.to_bytes(4, 'big')


def invented_program():
    data = bytearray(0x900000)
    for fighter in range(64):
        set_pointer(data, fighter, SETS + 16 * min(fighter, 0x24))  # $25-$3F share fighter $24's set
    for fighter in range(0x25):
        data[SETS + 16 * fighter:SETS + 16 * fighter + 16] = bytes([fighter, 0x5A] * 8)
    return data


def run(data, temp, fighter='0x1e', digest=None):
    source, output = Path(temp) / 'input.bin', Path(temp) / 'output.bin'
    source.write_bytes(data)
    result = subprocess.run([sys.executable, str(TOOL), str(source), str(output),
                             '--sha256', digest or hashlib.sha256(data).hexdigest(),
                             '--fighter-id', fighter], capture_output=True, text=True)
    return result, source, output


def test_command_gives_imported_slot_its_source_fighters_set():
    with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
        data = invented_program()
        result, source, output = run(data, temp, fighter='0x08')
        assert result.returncode == 0, result.stderr
        assert source.read_bytes() == data
        out = output.read_bytes()
        assert pointer(out, 0x30) == pointer(data, 0x08)
        changed = [i for i, (a, b) in enumerate(zip(data, out)) if a != b]
        assert changed and all(IMPORTED_ENTRY <= i < IMPORTED_ENTRY + 4 for i in changed)
        assert 'SHA-256' in result.stdout


def test_command_keeps_original_and_other_unused_entries():
    with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
        data = invented_program()
        result, _, output = run(data, temp)
        assert result.returncode == 0, result.stderr
        out = output.read_bytes()
        assert all(pointer(out, i) == pointer(data, i) for i in range(64) if i != 0x30)
        assert out[SETS:SETS + 16 * 0x25] == data[SETS:SETS + 16 * 0x25]


def test_command_refuses_unexpected_tables_and_inputs_without_writing():
    def changed(fighter, value):
        data = invented_program()
        set_pointer(data, fighter, value)
        return data

    moved_default = invented_program()
    for fighter in range(0x25, 64):
        set_pointer(moved_default, fighter, SETS)

    cases = (
        (changed(0x31, SETS), '0x1e', None, 'shared default'),           # one unused entry differs
        (changed(0x30, SETS + 16 * 0x1E), '0x1e', None, 'already'),       # $30 already has its own entry
        (moved_default, '0x1e', None, 'shared default'),                  # default is not fighter $24's set
        (changed(0x05, 0x8FFFF8), '0x1e', None, 'outside'),               # set runs past the program
        (changed(0x05, 0x2F0000), '0x1e', None, 'outside'),               # set in the banked window
        (changed(0x05, TABLE + 0x40), '0x1e', None, 'on the table'),      # set overlaps the pointers
        (changed(0x08, SETS + 16 * 0x24), '0x08', None, 'no own set'),    # source shares the default
        (invented_program(), '0x25', None, 'original fighter'),
        (invented_program(), '0x1e', '0' * 64, 'SHA-256'),
    )
    for data, fighter, digest, message in cases:
        with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
            result, _, output = run(data, temp, fighter=fighter, digest=digest)
            assert result.returncode == 1, message
            assert message in result.stderr
            assert not output.exists()


def test_command_refuses_paths_outside_private_and_existing_output():
    with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
        data = invented_program()
        Path(temp, 'output.bin').write_bytes(b'kept')
        result, _, output = run(data, temp)
        assert result.returncode == 1
        assert output.read_bytes() == b'kept'
    with tempfile.TemporaryDirectory() as temp:
        result, _, output = run(invented_program(), temp)
        assert result.returncode == 1 and 'private/' in result.stderr
        assert not output.exists()
