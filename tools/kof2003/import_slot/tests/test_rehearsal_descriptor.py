"""The rehearsal descriptor command operates on invented text only."""
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TOOL = ROOT / 'tools/kof2003/import_slot/rehearsal_descriptor.py'


def test_descriptor_reuses_original_pairs_in_added_space():
    with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
        source, dest = Path(temp) / 'input.c', Path(temp) / 'output.c'
        data = (b'.crom_size = 0x4000000,\n.crom_pairs = {\n'
                b'    {"a", "b"},\n    {"c", "d"},\n'
                b'    {"e", "f"},\n    {"g", "h"},\n},\n')
        source.write_bytes(data)
        run = subprocess.run([sys.executable, str(TOOL), str(source), str(dest),
                              '--sha256', hashlib.sha256(data).hexdigest()], capture_output=True, text=True)
        assert run.returncode == 0, run.stderr
        result = dest.read_bytes()
        assert source.read_bytes() == data
        assert b'.crom_size = 0x8000000,' in result
        for pair in (b'{"a", "b"}', b'{"c", "d"}', b'{"e", "f"}', b'{"g", "h"}'):
            assert result.count(pair) == 2
