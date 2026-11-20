"""The native player's probe (native_probe.c), compiled against a fake bus (ticket 08).

The fake bus returns invented numbers derived from the address and the frame; no game
memory is involved. Skipped when no C compiler is installed.
"""
import os
import shutil
import subprocess

import pytest

from match.probe_log import parse_spec, read_log

SOURCE = __import__("pathlib").Path(__file__).resolve().parents[1] / "native_probe.c"
COMPILER = next((c for c in (os.environ.get("CC"), "clang", "gcc", "cc") if c and shutil.which(c)), None)

HARNESS = r"""
#include <stdint.h>
#include <stdlib.h>
void kof_native_probe(long frame);
static long now;
/* Word at A in frame F: high byte (A >> 8) + F, low byte A. */
uint16_t bus_peek16(uint32_t a) {
    if (a & 1) abort();  /* the bus reads whole words only */
    return (uint16_t)((((a >> 8) + now) & 0xff) << 8 | (a & 0xff));
}
int main(int argc, char **argv) {
    long frames = argc > 1 ? strtol(argv[1], NULL, 10) : 0;
    for (now = 0; now < frames; now++) kof_native_probe(now);
    return 0;
}
"""

pytestmark = pytest.mark.skipif(COMPILER is None, reason="no C compiler")


@pytest.fixture(scope="module")
def harness(tmp_path_factory):
    work = tmp_path_factory.mktemp("native-probe")
    (work / "harness.c").write_text(HARNESS)
    exe = work / ("harness.exe" if os.name == "nt" else "harness")
    subprocess.run([COMPILER, "-std=c11", "-Wall", "-Wextra", "-Werror", str(SOURCE),
                    str(work / "harness.c"), "-o", str(exe)], check=True)
    return exe


def run(harness, tmp_path, frames=3, **env):
    environment = {k: v for k, v in os.environ.items() if not k.startswith("KOF_NATIVE_PROBE")}
    environment.update(env)
    return subprocess.run([str(harness), str(frames)], env=environment, cwd=tmp_path,
                          capture_output=True, text=True, check=True)


def test_without_the_option_nothing_is_written(harness, tmp_path):
    result = run(harness, tmp_path)
    assert result.stderr == ""
    assert list(tmp_path.iterdir()) == []


def test_one_line_per_frame_with_each_requested_address(harness, tmp_path):
    log = tmp_path / "probe.tsv"
    spec = "0x1010e0:4,0x2fe91d:1,0x2fe91c:1,0x102eac:2"
    run(harness, tmp_path, KOF_NATIVE_PROBE=spec, KOF_NATIVE_PROBE_LOG=str(log))
    assert read_log(log.read_text(), columns=len(parse_spec(spec))) == {
        0: ("10e010e2", "1c", "e9", "2eac"),
        1: ("11e011e2", "1c", "ea", "2fac"),
        2: ("12e012e2", "1c", "eb", "30ac"),
    }


def test_first_frame_option_skips_earlier_frames(harness, tmp_path):
    log = tmp_path / "probe.tsv"
    run(harness, tmp_path, frames=5, KOF_NATIVE_PROBE="0x100000:1", KOF_NATIVE_PROBE_LOG=str(log),
        KOF_NATIVE_PROBE_FIRST="3")
    assert log.read_text() == "3\t03\n4\t04\n"


@pytest.mark.parametrize("spec", ["0x1010e1:2", "0x1010e0:3", "1010e0:1", "0x1000000:1",
                                  ",".join(["0x100000:1"] * 17)])
def test_an_invalid_address_list_is_reported_and_writes_nothing(harness, tmp_path, spec):
    log = tmp_path / "probe.tsv"
    result = run(harness, tmp_path, KOF_NATIVE_PROBE=spec, KOF_NATIVE_PROBE_LOG=str(log))
    assert "[probe] invalid KOF_NATIVE_PROBE" in result.stderr
    assert not log.exists()


def test_the_log_path_is_required(harness, tmp_path):
    result = run(harness, tmp_path, KOF_NATIVE_PROBE="0x100000:1")
    assert "[probe] KOF_NATIVE_PROBE_LOG" in result.stderr
    assert list(tmp_path.iterdir()) == []
