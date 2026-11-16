"""Comparing two capture sets by hash.

The files here hold made-up bytes, not game graphics. Expected values are
written out by hand.
"""
import pytest

from match.compare_captures import compare, hash_set, main


def write_set(directory, frames):
    directory.mkdir(parents=True)
    for frame, content in frames.items():
        (directory / f"frame-{frame:05d}.png").write_bytes(content)
    return directory


def test_equal_sets_report_equal(tmp_path):
    a = write_set(tmp_path / "a", {600: b"boot", 3000: b"select"})
    b = write_set(tmp_path / "b", {600: b"boot", 3000: b"select"})

    result = compare(a, b)

    assert result.equal
    assert result.first_difference is None
    assert result.frames_compared == 2


def test_one_differing_frame_is_reported_by_number(tmp_path):
    a = write_set(tmp_path / "a", {600: b"boot", 3000: b"select", 5400: b"fight"})
    b = write_set(tmp_path / "b", {600: b"boot", 3000: b"select", 5400: b"fighT"})

    result = compare(a, b)

    assert not result.equal
    assert result.first_difference == (5400, "differs")


def test_first_difference_is_the_lowest_frame(tmp_path):
    a = write_set(tmp_path / "a", {600: b"x", 3000: b"y", 5400: b"z"})
    b = write_set(tmp_path / "b", {600: b"x", 3000: b"Y", 5400: b"Z"})

    assert compare(a, b).first_difference == (3000, "differs")


def test_a_frame_missing_from_the_second_set(tmp_path):
    a = write_set(tmp_path / "a", {600: b"boot", 3000: b"select"})
    b = write_set(tmp_path / "b", {600: b"boot"})

    assert compare(a, b).first_difference == (3000, "missing in second")


def test_a_frame_missing_from_the_first_set(tmp_path):
    a = write_set(tmp_path / "a", {600: b"boot"})
    b = write_set(tmp_path / "b", {600: b"boot", 3000: b"select"})

    assert compare(a, b).first_difference == (3000, "missing in first")


def test_two_empty_sets_are_not_a_valid_comparison(tmp_path):
    a = write_set(tmp_path / "a", {})
    b = write_set(tmp_path / "b", {})

    with pytest.raises(ValueError, match="no captures"):
        compare(a, b)


def test_hash_set_ignores_other_files(tmp_path):
    a = write_set(tmp_path / "a", {600: b"boot"})
    (a / "player.log").write_text("not a capture")

    assert list(hash_set(a)) == [600]


def test_command_line_exit_codes(tmp_path, capsys):
    a = write_set(tmp_path / "a", {600: b"boot"})
    same = write_set(tmp_path / "same", {600: b"boot"})
    other = write_set(tmp_path / "other", {600: b"bOot"})

    assert main([str(a), str(same)]) == 0
    assert "equal" in capsys.readouterr().out
    assert main([str(a), str(other)]) == 1
    assert "frame 600" in capsys.readouterr().out
