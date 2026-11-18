"""Check the optional monitoring hook using an invented private source file."""
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TOOL = ROOT / 'tools/kof2003/import_slot/monitor_hook.py'


def test_command_adds_optional_hook_without_changing_input():
    with tempfile.TemporaryDirectory(dir=ROOT / 'private/work') as temp:
        source, dest = Path(temp) / 'input.c', Path(temp) / 'output.c'
        data = b'void run(void) {\n    run_frame();\n}\n'
        source.write_bytes(data)
        run = subprocess.run([sys.executable, str(TOOL), str(source), str(dest),
                              '--sha256', hashlib.sha256(data).hexdigest()], capture_output=True, text=True)
        assert run.returncode == 0, run.stderr
        assert source.read_bytes() == data
        result = dest.read_bytes()
        assert b'#ifdef KOF2003_REHEARSAL_MONITOR' in result
        assert b'kof_rehearsal_monitor(frame, &in);' in result
        assert result.index(b'run_frame();') < result.index(b'kof_rehearsal_monitor(frame, &in);')
