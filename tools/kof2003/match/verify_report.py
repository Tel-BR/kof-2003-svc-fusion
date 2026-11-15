"""Summary of a native player run with --verify.

The player's exit code does not reflect state mismatches or interpreter
fallback, so acceptance reads these counts from its log.
"""
import re
from dataclasses import dataclass

VERIFY = re.compile(
    r"^\[verify\] (\d+) blocks checked, (\d+) mismatches, (\d+) cycle-count differences", re.M)
EXEC = re.compile(
    r"^\[exec\] native blocks \d+, native instructions (\d+), interpreted instructions (\d+) "
    r"\(([\d.]+)% native\), (\d+) uncovered entry points", re.M)


@dataclass(frozen=True)
class Report:
    blocks_checked: int
    mismatches: int
    cycle_differences: int
    native_instructions: int
    interpreted_instructions: int
    native_percent: str
    uncovered_entry_points: int


def read_report(log):
    verify, executed = VERIFY.search(log), EXEC.search(log)
    if not (verify and executed):
        raise ValueError("no --verify summary in the player log; the run did not finish")
    blocks, mismatches, cycles = (int(v) for v in verify.groups())
    native, interpreted, percent, uncovered = executed.groups()
    return Report(blocks, mismatches, cycles, int(native), int(interpreted), percent, int(uncovered))
