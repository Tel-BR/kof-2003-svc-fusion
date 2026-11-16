"""Build and run the synthetic grown-loader test (graphics-set-growth, issue 03).

One command, from tools/kof2003:

    py -3 -m loader.run_loader_test

The toolkit is third-party code kept under private/. Point NEOGEORECOMP_SOURCE at it,
or leave it unset to use private/work/samsho-runtime-source/neogeorecomp. The test uses
no game data; it writes 80 MiB of synthetic files into a temporary folder under
private/work/graphics-growth/loader-test/ (override with LOADER_TEST_WORK) and removes
them afterwards.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
DEFAULT_TOOLKIT = REPO / "private" / "work" / "samsho-runtime-source" / "neogeorecomp"
DEFAULT_WORK = REPO / "private" / "work" / "graphics-growth" / "loader-test"


def find_compiler():
    for name in (os.environ.get("CC"), "clang", "gcc", "cc"):
        if name and shutil.which(name):
            return name
    sys.exit("error: no C compiler found (set CC, or install clang or gcc)")


def main():
    toolkit = Path(os.environ.get("NEOGEORECOMP_SOURCE", DEFAULT_TOOLKIT))
    if not (toolkit / "src" / "video.c").exists():
        sys.exit(f"error: toolkit not found at {toolkit}; set NEOGEORECOMP_SOURCE")
    work = Path(os.environ.get("LOADER_TEST_WORK", DEFAULT_WORK))
    work.mkdir(parents=True, exist_ok=True)
    exe = work / ("test_grown_loader.exe" if os.name == "nt" else "test_grown_loader")
    cmd = [find_compiler(), "-std=c11", "-O1", "-Wall", "-Wextra", "-Wno-unused-function",
           "-I", str(toolkit / "src"), "-I", str(toolkit / "include"),
           str(HERE / "test_grown_loader.c"), str(toolkit / "src" / "romload.c"),
           "-o", str(exe)]
    if subprocess.run(cmd).returncode != 0:
        sys.exit("error: the test did not compile; see the compiler output above")
    files = work / "files"
    files.mkdir(exist_ok=True)
    try:
        return subprocess.run([str(exe), str(files)]).returncode
    finally:
        shutil.rmtree(files, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
