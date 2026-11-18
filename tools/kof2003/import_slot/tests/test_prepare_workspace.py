"""Exercise the preparation command with invented files, never game data."""
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TOOL = ROOT / "tools" / "kof2003" / "import_slot" / "prepare_workspace.py"


def temporary_area():
    work = ROOT / "private" / "work"
    work.mkdir(parents=True, exist_ok=True)
    return tempfile.TemporaryDirectory(dir=work)


def test_preparation_makes_an_independent_private_copy():
    with temporary_area() as temporary:
        area = Path(temporary)
        source = area / "source"
        source.mkdir()
        (source / "271-pd.bin").write_bytes(b"invented program")
        (source / "sp-s2.sp1").write_bytes(b"invented bios")
        destination = area / "experiment"
        result = subprocess.run([sys.executable, str(TOOL), str(source), str(destination)],
                                capture_output=True, text=True)
        assert result.returncode == 0, result.stderr
        (destination / "271-pd.bin").write_bytes(b"changed experiment")
        assert (source / "271-pd.bin").read_bytes() == b"invented program"
        assert (destination / "sp-s2.sp1").read_bytes() == b"invented bios"


def test_preparation_refuses_to_overwrite_an_existing_experiment():
    with temporary_area() as temporary:
        area = Path(temporary)
        source = area / "source"
        source.mkdir()
        (source / "271-pd.bin").write_bytes(b"invented program")
        (source / "sp-s2.sp1").write_bytes(b"invented bios")
        destination = area / "experiment"
        destination.mkdir()
        (destination / "271-pd.bin").write_bytes(b"earlier experiment")
        result = subprocess.run([sys.executable, str(TOOL), str(source), str(destination)],
                                capture_output=True, text=True)
        assert result.returncode != 0
        assert (destination / "271-pd.bin").read_bytes() == b"earlier experiment"
