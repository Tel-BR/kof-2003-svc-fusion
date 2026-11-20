"""Recreate an input script from invented monitor events through the CLI."""
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TOOL = ROOT / 'tools/kof2003/import_slot/replay_recording.py'


def test_command_preserves_input_edges_and_private_output():
    with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
        source, dest = Path(temp) / 'input.log', Path(temp) / 'replay.txt'
        source.write_text('[rehearsal-input] frame=0 p1=00 start=0 coin=0\n'
                          '[rehearsal-input] frame=10 p1=02 start=0 coin=0\n'
                          '[rehearsal-input] frame=13 p1=0a start=0 coin=0\n'
                          '[rehearsal-input] frame=15 p1=18 start=0 coin=0\n'
                          '[rehearsal-input] frame=18 p1=00 start=0 coin=0\n'
                          '[rehearsal-frame] 20 0000 0000 0000 0000\n')
        result = subprocess.run([sys.executable, str(TOOL), str(source), str(dest)],
                                capture_output=True, text=True)
        assert result.returncode == 0, result.stderr
        assert dest.read_text().splitlines() == ['10-12 down', '13-14 down+right', '15-17 right+a']


def test_command_rejects_out_of_order_events_without_output():
    with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
        source, dest = Path(temp) / 'input.log', Path(temp) / 'replay.txt'
        source.write_text('[rehearsal-input] frame=10 p1=02 start=0 coin=0\n'
                          '[rehearsal-input] frame=9 p1=00 start=0 coin=0\n'
                          '[rehearsal-frame] 20 0000 0000 0000 0000\n')
        result = subprocess.run([sys.executable, str(TOOL), str(source), str(dest)],
                                capture_output=True, text=True)
        assert result.returncode != 0
        assert not dest.exists()
