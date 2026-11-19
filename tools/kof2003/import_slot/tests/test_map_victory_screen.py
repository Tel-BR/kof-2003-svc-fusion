"""Exercise the victory-screen ID mapping command with invented program contents."""
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TOOL = ROOT / 'tools/kof2003/import_slot/map_victory_screen.py'
SITE, SITE_BYTES = 0xE202, bytes.fromhex('12f010005241')
MAP_TABLE, MAP_ROUTINE = 0x53100, 0x53140
ROUTINE = (b'\x2f\x08\x41\xf9' + MAP_TABLE.to_bytes(4, 'big') + b'\x10\x30\x00\x00\x20\x5f\x4e\x75')
TRAMPOLINE = 0x53200


def invented_program():
    data = bytearray(0x900000)
    data[0x52B60:0x60000] = b'\xff' * (0x60000 - 0x52B60)
    data[SITE:SITE + 6] = SITE_BYTES
    data[MAP_TABLE:MAP_TABLE + 64] = bytes(range(0x30)) + b'\x1e' + bytes(range(0x31, 64))
    data[MAP_ROUTINE:MAP_ROUTINE + 16] = ROUTINE
    return data


def run(data, temp):
    source, dest = Path(temp) / 'input.bin', Path(temp) / 'output.bin'
    source.write_bytes(data)
    result = subprocess.run([sys.executable, str(TOOL), str(source), str(dest), '--sha256',
                             hashlib.sha256(data).hexdigest()], capture_output=True, text=True)
    return result, source, dest


def test_command_routes_the_team_copy_through_the_presentation_map():
    with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
        data = invented_program()
        result, source, dest = run(data, temp)
        assert result.returncode == 0, result.stderr
        assert source.read_bytes() == data
        out = dest.read_bytes()
        # The six-byte copy now calls the routine; nothing else of the program changed outside it.
        assert out[SITE:SITE + 6] == b'\x4e\xb9' + TRAMPOLINE.to_bytes(4, 'big')
        changed = [i for i, (a, b) in enumerate(zip(data, out)) if a != b]
        assert all(i in range(SITE, SITE + 6) or i in range(TRAMPOLINE, TRAMPOLINE + 0x40) for i in changed)
        body = out[TRAMPOLINE:TRAMPOLINE + 0x40]
        # It reads the team byte, keeps colour bits 7-6, maps the low six bits through the map,
        # stores the byte, repeats the displaced `addq.w #1,d1` and returns.
        assert b'\x10\x30\x10\x00' in body and b'\x4e\xb9' + MAP_ROUTINE.to_bytes(4, 'big') in body
        assert b'\x02\x57\x00\xc0' in body and b'\x02\x40\x00\x3f' in body and b'\x12\xc0' in body
        assert body.index(b'\x52\x41\x4e\x75') + 4 <= len(body)


def test_command_rejects_missing_map_unexpected_site_and_used_space():
    for mutate, message in (
            (lambda d: d.__setitem__(MAP_ROUTINE, 0), 'presentation map routine is missing'),
            (lambda d: d.__setitem__(SITE, 0x13), 'unexpected victory-screen team copy'),
            (lambda d: d.__setitem__(TRAMPOLINE + 3, 0), 'is not empty')):
        with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
            data = invented_program()
            mutate(data)
            result, _, dest = run(data, temp)
            assert result.returncode == 1 and message in result.stderr
            assert not dest.exists()


def test_command_refuses_a_wrong_hash_and_paths_outside_private():
    with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
        data = invented_program()
        source, dest = Path(temp) / 'input.bin', Path(temp) / 'output.bin'
        source.write_bytes(data)
        result = subprocess.run([sys.executable, str(TOOL), str(source), str(dest), '--sha256', '0' * 64],
                                capture_output=True, text=True)
        assert result.returncode == 1 and 'SHA-256' in result.stderr and not dest.exists()
    with tempfile.TemporaryDirectory() as temp:
        data = invented_program()
        result, _, dest = run(data, temp)
        assert result.returncode == 1 and 'inside private' in result.stderr and not dest.exists()
