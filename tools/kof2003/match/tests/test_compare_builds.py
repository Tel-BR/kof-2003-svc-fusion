"""Comparing two builds on one script, with a fake player.

The fake writes made-up capture bytes, not game graphics.
"""
from match.compare_builds import compare_one
from match.repeat_reference import PLANS
from match.verify_report import Report


def fake_player(content_for):
    def runs(script, frames, shots, out, player, runner=None):
        out.mkdir(parents=True)
        for frame in shots:
            (out / f"frame-{frame:05d}.png").write_bytes(content_for(player.parent.name, frame))
        if runner:
            runner(["fake"], None)
        return Report(10, 0, 0, 100, 0, "100.0", 0)
    return runs


def test_same_output_from_both_builds_is_equal(tmp_path):
    runs = fake_player(lambda build, frame: b"same %d" % frame)

    result, ref, cand, memory = compare_one("coin-start", tmp_path / "a", tmp_path / "b",
                                            tmp_path / "out", runs=runs)

    assert result.equal
    assert result.frames_compared == len(PLANS["coin-start"]["shots"])
    assert memory == []


def test_one_different_frame_from_the_candidate_is_reported(tmp_path):
    runs = fake_player(lambda build, frame: b"x" if build == "a" else (b"y" if frame == 3000 else b"x"))

    result, *_ = compare_one("coin-start", tmp_path / "a", tmp_path / "b", tmp_path / "out", runs=runs)

    assert not result.equal
    assert result.first_difference == (3000, "differs")


def test_candidate_memory_is_measured_through_the_runner(tmp_path):
    runs = fake_player(lambda build, frame: b"same")

    *_, memory = compare_one("coin-start", tmp_path / "a", tmp_path / "b", tmp_path / "out",
                             measure=lambda command, stream: "measured", runs=runs)

    assert memory == ["measured"]


def test_verify_is_worse_only_when_a_failure_count_grows():
    from match.compare_builds import worse
    ref = Report(1000, 0, 0, 100, 0, "100.0", 2)
    assert not worse(Report(990, 0, 0, 100, 0, "100.0", 2), ref)  # fewer blocks checked is fine
    assert worse(Report(1000, 1, 0, 100, 0, "100.0", 2), ref)
    assert worse(Report(1000, 0, 1, 100, 0, "100.0", 2), ref)
    assert worse(Report(1000, 0, 0, 100, 0, "100.0", 3), ref)
