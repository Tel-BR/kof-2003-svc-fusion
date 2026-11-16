"""Running build C against build B, with a fake player.

The fake writes capture files the test builds itself, not game graphics.
"""
import pytest

from growth import run_added_space as proof
from growth.tests.test_verify_added_space import argb_rows, paint_tile, write_png
from growth.verify_added_space import Result
from match.verify_report import Report

CLEAN = Report(10, 0, 0, 100, 0, "100.0", 0)


def fake_player(tile_in):
    """A player that paints the synthetic tile in the builds `tile_in` names."""
    def runs(script, frames, shots, out, player, runner=None, rom_path=None):
        out.mkdir(parents=True)
        for frame in shots:
            rows = argb_rows(320, 224, (frame % 7, 0, 0))
            if out.name in tile_in:
                paint_tile(rows, 152, 96, 0)
            write_png(out / f"frame-{frame:05d}.png", 320, 224, rows)
        return Report(10, 0, 0, 100, 0, "100.0", 0)
    return runs


def plan():
    return {"frames": 10, "shots": [2000, 3000]}


def script(tmp_path):
    path = tmp_path / "coin-start.txt"
    path.write_text("1200 coin\n2400 start\n")
    return path


def test_the_tile_in_the_candidate_alone_passes(tmp_path):
    results, reports = proof.run_both(script(tmp_path), tmp_path / "c", tmp_path / "b",
                                      tmp_path / "out", tmp_path / "roms", plan(),
                                      runs=fake_player({"candidate"}))

    assert sorted(results) == [2000, 3000]
    assert all(result.matched for result in results.values())
    assert not any(result.reference_matched for result in results.values())
    assert len(reports) == 2


def test_the_tile_missing_from_the_candidate_is_reported(tmp_path):
    results, _ = proof.run_both(script(tmp_path), tmp_path / "c", tmp_path / "b",
                                tmp_path / "out", tmp_path / "roms", plan(),
                                runs=fake_player(set()))

    assert not any(result.matched for result in results.values())


def test_a_frame_before_the_first_one_the_planter_touches_is_refused(tmp_path):
    early = {"frames": 10, "shots": [600]}

    with pytest.raises(ValueError, match="leaves the board alone"):
        proof.run_both(script(tmp_path), tmp_path / "c", tmp_path / "b", tmp_path / "out",
                       tmp_path / "roms", early, runs=fake_player({"candidate"}))


def test_the_tile_in_both_builds_is_reported(tmp_path):
    results, _ = proof.run_both(script(tmp_path), tmp_path / "c", tmp_path / "b",
                                tmp_path / "out", tmp_path / "roms", plan(),
                                runs=fake_player({"candidate", "reference"}))

    assert all(result.reference_matched for result in results.values())


def test_a_frame_without_the_tile_fails_the_run():
    results = {600: Result((152, 96), True, 0, False),
               2000: Result((152, 96), False, 31, False)}

    assert proof.failures(results, (CLEAN, CLEAN)) == [
        "frame 2000: the candidate does not show the tile (31 of 256 pixels differ)"]


def test_the_tile_in_the_reference_fails_the_run():
    results = {600: Result((152, 96), True, 0, True)}

    assert proof.failures(results, (CLEAN, CLEAN)) == [
        "frame 600: the reference shows the tile too, so it proves nothing"]


def test_a_state_mismatch_in_verify_fails_the_run():
    results = {600: Result((152, 96), True, 0, False)}
    broken = Report(10, 3, 0, 100, 0, "100.0", 0)

    assert proof.failures(results, (CLEAN, broken)) == [
        "reference: 3 state mismatches in --verify"]


def test_every_frame_showing_the_tile_and_nothing_else_wrong_passes():
    results = {600: Result((152, 96), True, 0, False), 2000: Result((152, 96), True, 0, False)}

    assert proof.failures(results, (CLEAN, CLEAN)) == []
