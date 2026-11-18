"""Check selection-table expansion with an invented program image."""
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TOOL = ROOT / 'tools/kof2003/import_slot/selection_table.py'


def test_new_selection_row_keeps_all_existing_cells_and_adds_clone():
    with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
        source, dest = Path(temp) / 'input.bin', Path(temp) / 'output.bin'
        data = bytearray(0x900000)
        data[0x52A20:0x52B60] = b'\xff' * 0x140
        for row in range(13):
            for column in range(3):
                at = 0x9856 + (row * 3 + column) * 6
                data[at:at + 6] = (100 + 20 * column).to_bytes(2, 'big') + (150 - row * 8).to_bytes(2, 'big') + (row * 3 + column).to_bytes(2, 'big')
        data[0x9523] = 10
        data[0x952A] = 0x12
        data[0x9556:0x9558] = (10).to_bytes(2, 'big')
        data[0x95DA:0x95DC] = (38).to_bytes(2, 'big')
        data[0x95E1] = 38
        # Invented instruction and displacement to the synthetic table.
        data[0x95FE:0x9602] = (0x1234).to_bytes(2, 'big') + (0x9856 - 0x9600).to_bytes(2, 'big', signed=True)
        data[0x9602:0x9608] = b'ABCDEF'
        source.write_bytes(data)
        run = subprocess.run([sys.executable, str(TOOL), str(source), str(dest),
                              '--sha256', hashlib.sha256(data).hexdigest()], capture_output=True, text=True)
        assert run.returncode == 0, run.stderr
        out = dest.read_bytes()
        assert out[0x52A20:0x52A20 + 39 * 6] == data[0x9856:0x9856 + 39 * 6]
        assert int.from_bytes(out[0x52A20 + 39 * 6 + 4:0x52A20 + 39 * 6 + 6], 'big') == 0x30
        assert out[0x9523] == 14 and out[0x95E1] == 44
        assert out[0x9602:0x9608] != data[0x9602:0x9608]
        assert b'ABCDEF' in out[0x52B30:0x52B60]
