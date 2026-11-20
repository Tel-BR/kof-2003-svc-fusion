"""Test the private-image preparation command using an invented diagnostic image."""
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TOOL = ROOT / 'tools/kof2003/import_slot/map_opponent_rows.py'
sys.path.insert(0, str(TOOL.parent))
from map_opponent_rows import CODE, ROUTINE, ROUTINE_END, SITES, TABLE  # noqa: E402


def invented_program():
    data = bytearray(0x900000)
    data[0x52E00:0x53400] = b'\xff' * 0x600
    # The former private diagnostic routine (agent-written, not game code):
    # load the opponent byte, replace ID 48 by 30, multiply by 42, return.
    data[0x52E00:0x52E12] = bytes.fromhex('102b001f0c0000306602701ec0fc002a4e75')
    for site in SITES:
        data[site - 2:site] = bytes.fromhex('7000')
        data[site:site + 8] = b'\x4e\xb9' + (0x52E00).to_bytes(4, 'big') + b'\x4e\x71'
    return data


def run(data, temp, proxy='0x1e', digest=None):
    source, output = Path(temp) / 'input.bin', Path(temp) / 'output.bin'
    source.write_bytes(data)
    result = subprocess.run([sys.executable, str(TOOL), str(source), str(output),
                             '--sha256', digest or hashlib.sha256(data).hexdigest(),
                             '--proxy', proxy], capture_output=True, text=True)
    return result, source, output


def test_command_replaces_diagnostic_with_independent_proxy_table():
    with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
        data = invented_program()
        result, source, output = run(data, temp, proxy='0x08')
        assert result.returncode == 0, result.stderr
        assert source.read_bytes() == data
        out = output.read_bytes()
        assert out[TABLE:TABLE + 0x25] == bytes(range(0x25))
        assert out[TABLE + 0x30] == 8
        assert all(out[TABLE + i] == 30 for i in range(0x25, 64) if i != 0x30)
        assert out[0x52E00:0x52E12] == b'\xff' * 18
        assert out[ROUTINE:ROUTINE + len(CODE)] == CODE
        assert out[ROUTINE + len(CODE):ROUTINE_END] == b'\xff' * (ROUTINE_END - ROUTINE - len(CODE))
        for site in SITES:
            assert out[site:site + 8] == b'\x4e\xb9' + ROUTINE.to_bytes(4, 'big') + b'\x4e\x71'
        changes = (i for i, (a, b) in enumerate(zip(data, out)) if a != b)
        assert all(any(s <= i < s + 8 for s in SITES) or 0x52E00 <= i < 0x52E12 or
                   TABLE <= i < ROUTINE_END for i in changes)
        assert 'SHA-256' in result.stdout


def test_command_refuses_uncertain_readers_and_occupied_space_without_writing():
    for address, value, message in (
            (SITES[0], 0, 'reader code'),
            (SITES[1] - 1, 1, 'reader code'),
            (0x52E0A, 0, 'diagnostic routine'),
            (TABLE + 63, 0, 'proxy area'),
            (ROUTINE_END - 1, 0, 'proxy area')):
        with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
            data = invented_program()
            data[address] = value
            result, source, output = run(data, temp)
            assert result.returncode == 1 and message in result.stderr
            assert not output.exists()
            assert source.read_bytes() == data


def test_command_requires_original_proxy_and_verified_input_identity():
    for proxy, digest, message in (('0x30', None, 'original fighter'),
                                   ('-1', None, 'original fighter'),
                                   ('0x1e', '0' * 64, 'SHA-256')):
        with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
            result, _, output = run(invented_program(), temp, proxy, digest)
            assert result.returncode == 1 and message in result.stderr
            assert not output.exists()


def test_command_preserves_existing_output_and_refuses_public_paths():
    with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
        output = Path(temp) / 'output.bin'
        output.write_bytes(b'keep my existing file')
        result, _, _ = run(invented_program(), temp)
        assert result.returncode == 1
        assert output.read_bytes() == b'keep my existing file'
    with tempfile.TemporaryDirectory() as temp:
        result, _, output = run(invented_program(), temp)
        assert result.returncode == 1 and 'inside private' in result.stderr
        assert not output.exists()
