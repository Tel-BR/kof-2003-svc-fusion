"""Check the private manual keyboard preparation on invented source text."""
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TOOL = ROOT / 'tools/kof2003/import_slot/manual_keys.py'


def test_command_maps_manual_player_one_keys_without_changing_source():
    with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
        source, dest = Path(temp) / 'input.c', Path(temp) / 'output.c'
        data = b' '.join(b'SDL_SCANCODE_' + name for name in
                         (b'UP', b'DOWN', b'LEFT', b'RIGHT', b'Z', b'X', b'C', b'V'))
        source.write_bytes(data)
        run = subprocess.run([sys.executable, str(TOOL), str(source), str(dest),
                              '--sha256', hashlib.sha256(data).hexdigest()], capture_output=True, text=True)
        assert run.returncode == 0, run.stderr
        assert source.read_bytes() == data
        assert dest.read_bytes() == b' '.join(b'SDL_SCANCODE_' + name for name in
                                             (b'SPACE', b'S', b'A', b'D', b'KP_4', b'KP_5', b'KP_1', b'KP_2'))
