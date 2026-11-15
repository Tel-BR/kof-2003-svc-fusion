"""Reading the native player's --verify summary.

The sample lines are the summary the local build printed for the 6,000-frame
control on 2026-11-13 (ticket 01). They carry counts only, no game data.
"""
from match.verify_report import read_report

CONTROL_LOG = """\
[neogeorecomp] kof2003: 18222 recompiled entry points
[verify] cycle delta in block at $000D5A: native 64 interp 60
[neogeorecomp] frame 5400 -> frame-5400.png
[verify] 3583419 blocks checked, 0 mismatches, 2669 cycle-count differences
[exec] native blocks 3583419, native instructions 118359669, interpreted instructions 0 (100.00% native), 0 uncovered entry points
[exec] 0 new entry points; C:\\x\\entries-verify.txt now lists 385
"""


def test_reads_the_control_summary():
    report = read_report(CONTROL_LOG)

    assert report.blocks_checked == 3583419
    assert report.mismatches == 0
    assert report.cycle_differences == 2669
    assert report.native_instructions == 118359669
    assert report.interpreted_instructions == 0
    assert report.native_percent == "100.00"
    assert report.uncovered_entry_points == 0


def test_a_run_that_stopped_before_its_summary_is_an_error():
    import pytest

    with pytest.raises(ValueError, match="no --verify summary"):
        read_report(CONTROL_LOG.split("[verify] 3583419")[0])
