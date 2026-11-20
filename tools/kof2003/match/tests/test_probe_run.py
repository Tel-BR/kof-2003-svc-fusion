"""Probing one script on the native player and on MAME, with fake runtimes (ticket 08).

The fakes write invented values, not game memory.
"""
from pathlib import Path

import pytest

from match import probe_run
from match.run import run_native

SCRIPT = "1200 coin\n2400 start\n"


def fake_native(values):
    def runner(command, stream, env=None):
        Path(env["KOF_NATIVE_PROBE_LOG"]).write_text("".join(f"{f}\t{v}\n" for f, v in values.items()))
        fake_native.calls.append((command, env))
    fake_native.calls = []
    return runner


def fake_mame(values):
    def runs(script, frames, shots, out, lua, environment):
        out.mkdir(parents=True)
        Path(environment["PROBE_LOG"]).write_text("".join(f"{f}\t{v}\n" for f, v in values.items()))
        fake_mame.calls.append((frames, shots, lua, environment))
    fake_mame.calls = []
    return runs


def probe(tmp_path, native, mame, spec="0x100000:1", **options):
    script = tmp_path / "match.txt"
    script.write_text(SCRIPT)
    return probe_run.probe(script, 3, spec, tmp_path / "out", player=Path("player.exe"),
                           rom_path=Path("roms"), native_runner=fake_native(native),
                           mame_runner=fake_mame(mame), **options)


def test_both_runtimes_get_the_same_addresses_and_the_logs_are_compared(tmp_path):
    result = probe(tmp_path, {0: "aa", 1: "bb", 2: "cc"}, {0: "aa", 1: "bb", 2: "cc"})
    assert result.equal and result.frames == 3
    command, env = fake_native.calls[0]
    assert env["KOF_NATIVE_PROBE"] == "0x100000:1"
    assert env["KOF_NATIVE_PROBE_LOG"] == str(tmp_path / "out" / "native" / "probe.tsv")
    assert "--verify" not in command and "--headless" in command and "--mute" in command
    assert command[command.index("--frames") + 1] == "3"
    frames, shots, lua, environment = fake_mame.calls[0]
    assert (frames, shots, lua) == (3, [], probe_run.PROBE_LUA)
    assert environment["PROBE_ADDRESSES"] == "0x100000:1"
    assert environment["REPLAY_OFFSET"] == "2"
    assert environment["PROBE_LOG"] == str(tmp_path / "out" / "mame" / "probe.tsv")


def test_a_difference_is_reported_with_its_frame(tmp_path):
    result = probe(tmp_path, {0: "aa", 1: "bb"}, {0: "aa", 1: "bc"})
    assert not result.equal and result.first.frame == 1


def test_shift_and_window_reach_the_comparison(tmp_path):
    result = probe(tmp_path, {0: "aa", 1: "bb", 2: "zz"}, {1: "aa", 2: "bb"}, shift=1, last=1)
    assert result.equal and result.frames == 2


def test_verify_can_be_requested(tmp_path):
    with pytest.raises(ValueError, match="--verify summary"):  # the fake player prints none
        probe(tmp_path, {0: "aa"}, {0: "aa"}, verify=True)
    assert "--verify" in fake_native.calls[0][0]


def test_a_player_without_the_probe_is_reported(tmp_path):
    script = tmp_path / "match.txt"
    script.write_text(SCRIPT)
    with pytest.raises(RuntimeError, match="KOF2003_NATIVE_PROBE"):
        probe_run.probe(script, 3, "0x100000:1", tmp_path / "out", player=Path("player.exe"),
                        rom_path=Path("roms"), native_runner=lambda command, stream, env=None: None,
                        mame_runner=fake_mame({0: "aa"}))


def test_an_invalid_address_list_is_refused_before_anything_runs(tmp_path):
    with pytest.raises(ValueError):
        probe(tmp_path, {}, {}, spec="0x100001:2")
    assert fake_native.calls == [] and fake_mame.calls == []


def test_native_run_without_environment_keeps_the_old_runner_contract(tmp_path):
    calls = []
    run_native(tmp_path / "s.txt", 10, [], tmp_path / "n", player=Path("p.exe"), rom_path=Path("r"),
               runner=lambda command, stream: calls.append(command), verify=False)
    assert "--verify" not in calls[0]
