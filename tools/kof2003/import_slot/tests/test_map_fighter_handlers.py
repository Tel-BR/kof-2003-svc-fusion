"""Exercise the fighter routine-index mapping command with invented program contents."""
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TOOL = ROOT / 'tools/kof2003/import_slot/map_fighter_handlers.py'
SITES = (0x2B314, 0x2B438)
SITE_BYTES = bytes.fromhex('c26c001ed241d241')
MAP_TABLE = 0x53100
TRAMPOLINE = 0x53280


def invented_program(source=0x1E):
    data = bytearray(0x900000)
    data[0x52B60:0x60000] = b'\xff' * (0x60000 - 0x52B60)
    for site in SITES:
        data[site - 2:site] = bytes.fromhex('723f')
        data[site:site + 8] = SITE_BYTES
    data[MAP_TABLE:MAP_TABLE + 64] = bytes(range(0x30)) + bytes([source]) + bytes(range(0x31, 64))
    return data


def run(data, temp):
    source, dest = Path(temp) / 'input.bin', Path(temp) / 'output.bin'
    source.write_bytes(data)
    result = subprocess.run([sys.executable, str(TOOL), str(source), str(dest), '--sha256',
                             hashlib.sha256(data).hexdigest()], capture_output=True, text=True)
    return result, source, dest


def test_command_maps_the_fighter_id_before_both_routine_table_lookups():
    with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
        data = invented_program()
        result, source, dest = run(data, temp)
        assert result.returncode == 0, result.stderr
        assert source.read_bytes() == data
        out = dest.read_bytes()
        # Each index computation becomes a call plus a nop; nothing else changed outside them
        # and the routine area.
        for site in SITES:
            assert out[site:site + 8] == b'\x4e\xb9' + TRAMPOLINE.to_bytes(4, 'big') + b'\x4e\x71'
            assert out[site - 2:site] == bytes.fromhex('723f')
        changed = [i for i, (a, b) in enumerate(zip(data, out)) if a != b]
        assert all(any(i in range(s, s + 8) for s in SITES) or i in range(TRAMPOLINE, TRAMPOLINE + 0x40)
                   for i in changed)
        body = out[TRAMPOLINE:TRAMPOLINE + 0x40]
        # It repeats `and.w ($1e,a4),d1`, saves a1, maps the ID through the presentation map,
        # restores a1, repeats the two doublings of the index and returns.
        expected = bytes.fromhex('c26c001e' '48e70040' '43f9') + MAP_TABLE.to_bytes(4, 'big') + \
            bytes.fromhex('12311000' '4cdf0200' 'd241d241' '4e75')
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


def test_command_rejects_missing_map_unexpected_sites_and_used_space():
    for mutate, message in (
            (lambda d: d.__setitem__(MAP_TABLE + 3, 9), 'presentation map is missing'),
            (lambda d: d.__setitem__(MAP_TABLE + 0x30, 0x30), 'presentation map is missing'),
            (lambda d: d.__setitem__(SITES[0], 0x13), 'unexpected routine index code'),
            (lambda d: d.__setitem__(SITES[1] - 1, 0x3E), 'unexpected routine index code'),
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
