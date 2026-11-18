"""Check the palette command with invented colours and program data."""
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TOOL = ROOT / 'tools/kof2003/import_slot/rehearsal_palettes.py'


def test_clone_gets_private_palette_blocks_and_opposite_hue_changes():
    with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
        source, dest = Path(temp) / 'input.bin', Path(temp) / 'output.bin'
        data = bytearray(0x900000)
        data[0x15A000:0x15A800] = b'\xff' * 0x800
        for index, base in enumerate((0x6090A, 0x6098A, 0x60A0A, 0x60A8A)):
            for fighter in (5, 0x30):
                data[base + fighter * 2:base + fighter * 2 + 2] = (0x20 + index * 0x10).to_bytes(2, 'big')
        # Invented colours: transparent entry, neutral and saturated green.
        for group in range(2):
            for slot in range(16):
                at = 0x100000 + (0x20 + group * 0x10 + slot) * 32
                data[at:at + 6] = bytes.fromhex('1234 0777 00e0')
        source.write_bytes(data)
        run = subprocess.run([sys.executable, str(TOOL), str(source), str(dest),
                              '--sha256', hashlib.sha256(data).hexdigest(),
                              '--fighter-id', '5'], capture_output=True, text=True)
        assert run.returncode == 0, run.stderr
        out = dest.read_bytes()
        for i, base in enumerate((0x6090A, 0x6098A, 0x60A0A, 0x60A8A)):
            assert int.from_bytes(out[base + 0x30 * 2:base + 0x31 * 2], 'big') == 0x2D00 + i * 16
            assert out[base + 5 * 2:base + 6 * 2] == data[base + 5 * 2:base + 6 * 2]
        for variant in range(4):
            at = 0x15A000 + variant * 0x200
            assert out[at:at + 2] == bytes.fromhex('1234')
            assert out[at + 2:at + 4] != bytes.fromhex('0777')
            assert out[at + 4:at + 6] != bytes.fromhex('00e0')
            for offset in (2, 4):
                before = int.from_bytes(data[0x100400 + (variant % 2) * 0x200 + offset:
                                             0x100402 + (variant % 2) * 0x200 + offset], 'big')
                after = int.from_bytes(out[at + offset:at + offset + 2], 'big')
                assert before & 0x8000 == after & 0x8000
                for high, low in ((8, 14), (4, 13), (0, 12)):
                    old = (((before >> high) & 15) << 1) | ((before >> low) & 1)
                    new = (((after >> high) & 15) << 1) | ((after >> low) & 1)
                    assert abs(old - new) <= 3
        assert out[0x15A004:0x15A006] != out[0x15A404:0x15A406]
        assert out[0x15A204:0x15A206] != out[0x15A604:0x15A606]
        assert out[0x15A404:0x15A406] != out[0x15A604:0x15A606]
