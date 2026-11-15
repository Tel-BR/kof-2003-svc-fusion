"""Owner-recorded sessions: the input log written by log_inputs.lua.

The log lists the frame (frames completed so far) and the buttons held from
then on, "-" meaning none. Expected values are written out by hand.
"""
import pytest

from match.input_script import parse
from match.session import continue_session, read_log


def test_reads_held_buttons_by_frame():
    log = "0\t-\n221\tcoin\n226\t-\n1342\tleft\n1420\t-\n1422\tright\n1423\ta+right\n"

    assert read_log(log) == [
        (0, frozenset()),
        (221, frozenset({"coin"})),
        (226, frozenset()),
        (1342, frozenset({"left"})),
        (1420, frozenset()),
        (1422, frozenset({"right"})),
        (1423, frozenset({"a", "right"})),
    ]


def test_a_log_overwritten_after_a_soft_reset_is_rejected():
    damaged = "0\t-\n221\tcoin\n226\t-\n\x00\x00\x00\x005370\ta+b+right\n1092\ta+b+right\n"

    with pytest.raises(ValueError, match="soft reset"):
        read_log(damaged)


def test_a_test_script_continues_the_session_from_the_cut():
    log = read_log("0\t-\n221\tcoin\n226\t-\n1300\tleft\n1420\t-\n")
    script = parse("1360-1363 a\n")

    assert continue_session(log, 1342, script) == [
        (0, frozenset()),
        (221, frozenset({"coin"})),
        (226, frozenset()),
        (1300, frozenset({"left"})),
        (1342, frozenset()),
        (1360, frozenset({"a"})),
        (1364, frozenset()),
    ]


def test_a_script_that_starts_before_the_cut_is_rejected():
    with pytest.raises(ValueError, match="starts before the cut"):
        continue_session(read_log("0\t-\n"), 1342, parse("1300 a\n"))


def test_a_script_starting_at_the_cut_replaces_the_release():
    log = read_log("0\t-\n1300\tleft\n1420\t-\n")

    assert continue_session(log, 1342, parse("1342-1345 a\n")) == [
        (0, frozenset()),
        (1300, frozenset({"left"})),
        (1342, frozenset({"a"})),
        (1346, frozenset()),
    ]
