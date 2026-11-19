"""Exercise the intro-opponent ID mapping command with invented program contents."""
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TOOL = ROOT / 'tools/kof2003/import_slot/map_intro_opponent.py'
SITE, SITE_BYTES = 0x40BE2, bytes.fromhex('122b001f3e3c0003')
MAP_TABLE = 0x53100
TRAMPOLINE = 0x53240


def invented_program(source=0x1E):
    data = bytearray(0x900000)
    data[0x52B60:0x60000] = b'\xff' * (0x60000 - 0x52B60)
    data[SITE:SITE + 8] = SITE_BYTES
    data[MAP_TABLE:MAP_TABLE + 64] = bytes(range(0x30)) + bytes([source]) + bytes(range(0x31, 64))
    return data


def run(data, temp):
    source, dest = Path(temp) / 'input.bin', Path(temp) / 'output.bin'
    source.write_bytes(data)
    result = subprocess.run([sys.executable, str(TOOL), str(source), str(dest), '--sha256',
                             hashlib.sha256(data).hexdigest()], capture_output=True, text=True)
    return result, source, dest


def test_command_maps_the_other_fighters_id_before_the_intro_row_scan():
    with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
        data = invented_program()
        result, source, dest = run(data, temp)
        assert result.returncode == 0, result.stderr
        assert source.read_bytes() == data
        out = dest.read_bytes()
        # The eight displaced bytes become a call plus a nop; nothing else changed outside them
        # and the trampoline area.
        assert out[SITE:SITE + 8] == b'\x4e\xb9' + TRAMPOLINE.to_bytes(4, 'big') + b'\x4e\x71'
        changed = [i for i, (a, b) in enumerate(zip(data, out)) if a != b]
        assert all(i in range(SITE, SITE + 8) or i in range(TRAMPOLINE, TRAMPOLINE + 0x40) for i in changed)
        body = out[TRAMPOLINE:TRAMPOLINE + 0x40]
        # It repeats the read of the other fighter's ID, saves a1, maps the ID through the
        # presentation map without touching d0, restores a1, repeats `move.w #3,d7` and returns.
        expected = bytes.fromhex('122b001f' '48e70040' '43f9') + MAP_TABLE.to_bytes(4, 'big') + \
            bytes.fromhex('12311000' '4cdf0200' '3e3c0003' '4e75')
        assert body.startswith(expected)
        assert set(body[len(expected):]) == {0xff}


def test_command_leaves_original_ids_unmapped_and_follows_the_source_fighter():
    # The mapped ID is the presentation map entry: identity for originals, the source fighter for $30.
    for source in (0x1E, 0x08):
        with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
            data = invented_program(source)
            result, _, dest = run(data, temp)
            assert result.returncode == 0, result.stderr
            out = dest.read_bytes()
            assert out[MAP_TABLE:MAP_TABLE + 64] == data[MAP_TABLE:MAP_TABLE + 64]
            assert out[MAP_TABLE + 0x30] == source
            assert all(out[MAP_TABLE + i] == i for i in range(0x25))


def test_command_rejects_missing_map_unexpected_site_and_used_space():
    for mutate, message in (
            (lambda d: d.__setitem__(MAP_TABLE + 3, 9), 'presentation map is missing'),
            (lambda d: d.__setitem__(MAP_TABLE + 0x30, 0x30), 'presentation map is missing'),
            (lambda d: d.__setitem__(SITE, 0x13), 'unexpected intro opponent read'),
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
