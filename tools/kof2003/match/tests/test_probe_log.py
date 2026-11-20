"""Probe address lists and per-frame logs, shared by the native player and MAME (ticket 08).

The logs here are invented numbers, not game memory.
"""
import pytest

from match.probe_log import Probe, compare, format_spec, parse_spec, read_log


def test_address_list_reads_hex_addresses_with_their_sizes():
    assert parse_spec("0x1010e0:4, 0x2fe91d:1,0x102eac:2") == (
        Probe(0x1010E0, 4), Probe(0x2FE91D, 1), Probe(0x102EAC, 2))


def test_address_list_round_trips():
    probes = (Probe(0x1010E0, 4), Probe(0x2FE91D, 1))
    assert parse_spec(format_spec(probes)) == probes


@pytest.mark.parametrize("bad", ["", "0x1010e0", "0x1010e0:3", "0x1010e1:2", "0x1010e2:4x",
                                 "0x1000000:1", "zz:1", "0x10:1,,0x11:1"])
def test_address_list_refuses_what_a_runtime_could_not_read(bad):
    with pytest.raises(ValueError):
        parse_spec(bad)


def test_address_list_has_at_most_sixteen_entries():
    parse_spec(",".join(f"0x{0x100000 + i:x}:1" for i in range(16)))
    with pytest.raises(ValueError):
        parse_spec(",".join(f"0x{0x100000 + i:x}:1" for i in range(17)))


def test_log_maps_each_frame_to_its_values():
    log = read_log("5\t0001a2b4\t70\n6\t0001a2c0\t6f\n", columns=2)
    assert log == {5: ("0001a2b4", "70"), 6: ("0001a2c0", "6f")}


def test_log_with_the_wrong_number_of_columns_is_refused():
    with pytest.raises(ValueError, match="line 2"):
        read_log("5\taa\tbb\n6\taa\n", columns=2)


def test_identical_logs_compare_equal_on_every_shared_frame():
    log = {1: ("aa",), 2: ("bb",), 3: ("cc",)}
    result = compare(log, dict(log))
    assert result.equal
    assert result.frames == 3
    assert result.first is None


def test_first_mismatch_names_frame_column_and_both_values():
    left = {1: ("aa", "70"), 2: ("bb", "70"), 3: ("cc", "6f")}
    right = {1: ("aa", "70"), 2: ("bb", "71"), 3: ("cd", "6e")}
    result = compare(left, right)
    assert not result.equal
    assert (result.first.frame, result.first.column, result.first.left, result.first.right) == (2, 1, "70", "71")
    assert result.mismatched_frames == 2
    assert result.first_by_column == {0: 3, 1: 2}


def test_shift_compares_left_frame_n_with_right_frame_n_plus_shift():
    left = {1: ("aa",), 2: ("bb",)}
    right = {2: ("aa",), 3: ("bb",), 4: ("zz",)}
    assert compare(left, right, shift=1).equal
    assert not compare(left, right).equal


def test_frame_window_limits_the_comparison():
    left = {1: ("aa",), 2: ("bb",), 3: ("cc",)}
    right = {1: ("aa",), 2: ("bb",), 3: ("xx",)}
    result = compare(left, right, last=2)
    assert result.equal and result.frames == 2
    assert compare(left, right, first=3).frames == 1


def test_frames_missing_from_one_side_are_counted_not_compared():
    result = compare({1: ("aa",), 2: ("bb",)}, {2: ("bb",), 3: ("cc",)})
    assert result.frames == 1 and result.equal
    assert result.missing == 2
