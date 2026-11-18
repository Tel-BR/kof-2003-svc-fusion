"""Exercise frame relocation through the command with invented program data."""
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TOOL = ROOT / 'tools/kof2003/import_slot/relocate_frames.py'


def test_command_copies_frames_to_new_directory_and_added_space():
    with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
        source, dest = Path(temp) / 'input.bin', Path(temp) / 'output.bin'
        data = bytearray(0x900000)
        data[0x2FB000:0x2FB010] = b'\xff' * 16
        for index, offset in ((5, 0x10000), (6, 0x10010), (0x30, 0x10000)):
            at = 0x200000 + index * 4
            data[at:at + 4] = offset.to_bytes(4, 'big')
        data[0x210000:0x210010] = bytes.fromhex('0001 00010101 0001 1234 80 0000000000')
        source.write_bytes(data)
        run = subprocess.run([sys.executable, str(TOOL), str(source), str(dest),
                              '--sha256', hashlib.sha256(data).hexdigest(),
                              '--fighter-id', '5'], capture_output=True, text=True)
        assert run.returncode == 0, run.stderr
        result = dest.read_bytes()
        assert result[0x210000:0x210010] == data[0x210000:0x210010]
        assert int.from_bytes(result[0x2000C0:0x2000C4], 'big') == 0xFB000
        assert result[0x2FB000:0x2FB010] == bytes.fromhex('0001 00010101 0009 1234 80 0000000000')
