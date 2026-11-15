"""Run one input script on the native player and on the MAME MVS reference.

Both runs are silent, start from power-on with no saved settings, and write
captures for the same frames. All output goes under private/ because the
captures contain game graphics.

    py -3 -m match.run SCRIPT --frames N --shot F [--shot F ...] [--only native|mame]
"""
import argparse
import os
import subprocess
from datetime import datetime
from pathlib import Path

from match.input_script import parse
from match.verify_report import read_report

ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / "private" / "work"
BUILD = WORK / "mvs-native-build"
PLAYER = BUILD / "KOF 2003.exe"
MAME = Path(os.environ.get("KOF2003_MAME", Path.home() / "MAME" / "mame.exe"))
REPLAY_LUA = Path(__file__).with_name("replay.lua")
NATIVE_MAX_SHOTS = 64  # MAX_SHOTS in the neogeorecomp player
MAME_UNAVAILABLE = frozenset({"select", "test"})  # no such field in replay.lua


def cached_path(name):
    for line in (BUILD / "CMakeCache.txt").read_text().splitlines():
        if line.startswith(name + ":PATH="):
            return Path(line.split("=", 1)[1])
    raise LookupError(f"{name} is not in the native build's CMake cache")


def shot_name(frame):
    return f"frame-{frame:05d}.png"


def run_native(script_path, frames, shots, out):
    if len(shots) > NATIVE_MAX_SHOTS:
        raise ValueError(f"the native player takes at most {NATIVE_MAX_SHOTS} captures per run")
    out.mkdir(parents=True)
    command = [str(PLAYER), "--headless", "--verify", "--mute",
               "--rom-path", str(cached_path("KOF2003_ROMS")), "--bios", "sp-s2.sp1",
               "--frames", str(frames), "--input", str(script_path)]
    for frame in shots:
        command += ["--screenshot", f"{frame}:{out / shot_name(frame)}"]
    log = out / "player.log"
    with log.open("w") as stream:
        subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT, check=True)
    return read_report(log.read_text())


def run_mame(script, frames, shots, out):
    used = set().union(*(event.buttons for event in script.events))
    if used & MAME_UNAVAILABLE:
        raise ValueError(f"MAME's MVS replay cannot press {sorted(used & MAME_UNAVAILABLE)}")
    out.mkdir(parents=True)
    transitions = out / "transitions.tsv"
    transitions.write_text("".join(
        f"{frame}\t{'+'.join(sorted(held)) or '-'}\n" for frame, held in script.transitions()))
    shot_list = out / "shots.tsv"
    shot_list.write_text("".join(f"{frame}\t{shot_name(frame)}\n" for frame in shots))
    environment = dict(os.environ, REPLAY_TRANSITIONS=str(transitions),
                       REPLAY_SHOTS=str(shot_list), REPLAY_FRAMES=str(frames))
    roms = f"{ROOT / 'private' / 'dumps' / 'kof2003'};{ROOT / 'private' / 'bios'}"
    command = [str(MAME), "kof2003", "-bios", "euro", "-noreadconfig", "-skip_gameinfo",
               "-rompath", roms, "-cfg_directory", str(out / "cfg"),
               "-nvram_directory", str(out / "nvram"), "-snapshot_directory", str(out),
               "-video", "none", "-sound", "none", "-nothrottle",
               "-seconds_to_run", str(frames // 59 + 60),  # safety stop; replay.lua exits first
               "-autoboot_script", str(REPLAY_LUA)]
    with (out / "mame.log").open("w") as stream:
        subprocess.run(command, cwd=MAME.parent, env=environment,
                       stdout=stream, stderr=subprocess.STDOUT, check=True)
    missing = [frame for frame in shots if not (out / "kof2003" / shot_name(frame)).exists()
               and not (out / shot_name(frame)).exists()]
    if missing:
        raise RuntimeError(f"MAME did not capture frames {missing}")


def main(argv=None):
    options = argparse.ArgumentParser()
    options.add_argument("script", type=Path)
    options.add_argument("--frames", type=int, required=True)
    options.add_argument("--shot", type=int, action="append", default=[])
    options.add_argument("--only", choices=["native", "mame"])
    args = options.parse_args(argv)
    script = parse(args.script.read_text())
    out = WORK / "team-match" / f"{args.script.stem}-{datetime.now():%Y%m%d-%H%M%S}"
    if args.only != "mame":
        report = run_native(args.script.resolve(), args.frames, args.shot, out / "native")
        print(report)
        if report.mismatches:
            raise SystemExit(f"{report.mismatches} state mismatches in the native run; see {out}")
    if args.only != "native":
        run_mame(script, args.frames, args.shot, out / "mame")
    print(out)


if __name__ == "__main__":
    main()
