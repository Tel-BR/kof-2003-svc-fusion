"""Exercise the ID-lookup wiring command with invented program contents."""
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TOOL = ROOT / 'tools/kof2003/import_slot/wire_slot_lookups.py'
GUARDS = ((0x166AE, 0x24), (0x240F6, 0x25), (0x2412A, 0x24), (0x27E0C, 0x24))
INTRO = ((0xA5DB6, 0x52C00, (0x407EA, 0x40866)), (0xA5E4A, 0x52D00, (0x409E8, 0x40C70)))
LONGS = (0x79672, 0x79772, 0xB8250, 0x62B9AC)
WORDS = (0x79872, 0x798F2)
HEADER = 0xB3204


def invented_program():
    data = bytearray(0x900000)
    for immediate, value in GUARDS:
        data[immediate - 2:immediate + 2] = b'\x0c\x40' + value.to_bytes(2, 'big')
    data[0x52B60:0x60000] = b'\xff' * (0x60000 - 0x52B60)
    for number, (table, _, references) in enumerate(INTRO):
        for row in range(64):
            data[table + 4 * row:table + 4 * row + 4] = bytes([number, row, 0xff, 0xff])
        for reference in references:
            data[reference:reference + 4] = table.to_bytes(4, 'big')
    for table in LONGS:
        for entry in range(64):
            value = 0x1000 + entry if entry < 37 else 0x100
            data[table + 4 * entry:table + 4 * entry + 4] = value.to_bytes(4, 'big')
    for table in WORDS:
        for entry in range(64):
            value = 0x200 + entry if entry < 37 else 0x80
            data[table + 2 * entry:table + 2 * entry + 2] = value.to_bytes(2, 'big')
    for entry in range(37):
        data[HEADER + 2 * entry:HEADER + 2 * entry + 2] = (0x14A + 0x200 * entry).to_bytes(2, 'big')
    return data


def run(data, temp, fighter='0x1e'):
    source, dest = Path(temp) / 'input.bin', Path(temp) / 'output.bin'
    source.write_bytes(data)
    result = subprocess.run([sys.executable, str(TOOL), str(source), str(dest), '--sha256',
                             hashlib.sha256(data).hexdigest(), '--fighter-id', fighter],
                            capture_output=True, text=True)
    return result, source, dest


def test_command_wires_lookups_and_keeps_original_entries():
    with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
        data = invented_program()
        result, source, dest = run(data, temp)
        assert result.returncode == 0, result.stderr
        assert source.read_bytes() == data
        out = dest.read_bytes()
        for immediate, value in GUARDS:
            assert int.from_bytes(out[immediate:immediate + 2], 'big') in (0x3F, 0x40)
            assert out[immediate - 2:immediate] == b'\x0c\x40'
        for number, (table, new, references) in enumerate(INTRO):
            for reference in references:
                assert int.from_bytes(out[reference:reference + 4], 'big') == new
            assert out[new:new + 37 * 4] == data[table:table + 37 * 4]
            assert out[new + 0x30 * 4:new + 0x31 * 4] == bytes([number, 0x1E, 0xff, 0xff])
            assert out[table:table + 256] == data[table:table + 256]
        for table in LONGS:
            assert out[table + 0xC0:table + 0xC4] == (0x101E).to_bytes(4, 'big')
            assert out[table:table + 37 * 4] == data[table:table + 37 * 4]
            assert out[table + 0x31 * 4:table + 0x100] == data[table + 0x31 * 4:table + 0x100]
        for table in WORDS:
            assert out[table + 0x60:table + 0x62] == (0x21E).to_bytes(2, 'big')
        assert out[HEADER + 0x60:HEADER + 0x62] == out[HEADER + 0x3C:HEADER + 0x3E]
        changed = sum(a != b for a, b in zip(data, out))
        assert changed < 600


def test_command_rejects_unexpected_guard_without_creating_output():
    with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
        data = invented_program()
        data[0x240F6:0x240F8] = b'\x00\x24'
        result, _, dest = run(data, temp)
        assert result.returncode == 1
        assert 'unexpected ID guard' in result.stderr
        assert not dest.exists()


def test_command_rejects_occupied_destination_and_missing_default():
    with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
        data = invented_program()
        data[0x52C10] = 0
        result, _, dest = run(data, temp)
        assert result.returncode == 1 and 'not empty' in result.stderr
        assert not dest.exists()
    with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
        data = invented_program()
        data[0x79672 + 0x3F * 4:0x79672 + 0x40 * 4] = b'\x00\x00\x00\x01'
        result, _, dest = run(data, temp)
        assert result.returncode == 1 and 'shared default' in result.stderr


def test_command_refuses_fighter_outside_original_roster():
    with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
        result, _, dest = run(invented_program(), temp, fighter='0x30')
        assert result.returncode == 1
        assert not dest.exists()
