"""Run a scripted test on a MAME Neo Geo game, optionally continuing an owner-recorded session.

    py -3 -m match.mame_run NAME --game svc --session LOG --cut 1342 --script "1360-1363 a" \
        --shots 1366,1372 --last 1420 [--probe]
    py -3 -m match.mame_run NAME --game svc --playback DIR/NAME.inp --shots 1435 --last 5700

With --session, the recorded inputs replay up to --cut, all buttons are released there, and
--script follows (";" separates script lines). Without --session, --script runs from power-on.
Captures and the probe log are labelled with the log's frame numbers plus one (--offset 1,
measured for SVC Chaos in ticket 03). --playback instead plays back an .inp recording and labels
captures with the log's own frame numbers. Output goes to private/work/mame-runs/<NAME>-<time>/.
"""
import argparse
import os
import subprocess
from datetime import datetime
from pathlib import Path

from match.input_script import parse
from match.session import continue_session, read_log

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MAME = Path(os.environ.get("KOF2003_MAME", Path.home() / "MAME" / "mame.exe"))


def write_transitions(path, transitions):
    path.write_text("".join(f"{f}\t{'+'.join(sorted(h)) or '-'}\n" for f, h in transitions))


def main(argv=None):
    options = argparse.ArgumentParser()
    options.add_argument("name")
    options.add_argument("--game", default="svc")
    options.add_argument("--bios", default="euro")
    options.add_argument("--session", type=Path)
    options.add_argument("--cut", type=int)
    options.add_argument("--script", default="")
    options.add_argument("--offset", default="1")
    options.add_argument("--playback", type=Path)
    options.add_argument("--shots", default="")
    options.add_argument("--last", type=int, required=True)
    options.add_argument("--probe", action="store_true")
    options.add_argument("--lua", type=Path, help="another autoboot script that runs replay.lua itself")
    args = options.parse_args(argv)
    if (args.session is None) != (args.cut is None):
        options.error("--session and --cut go together")

    out = ROOT / "private" / "work" / "mame-runs" / f"{args.name}-{datetime.now():%Y%m%d-%H%M%S}"
    (out / "cfg").mkdir(parents=True)
    (out / "nvram").mkdir()
    shots = [int(s) for s in args.shots.split(",") if s]
    environment = dict(os.environ, REPLAY_FRAMES=str(args.last), REPLAY_OFFSET=args.offset,
                       REPLAY_LUA=str(HERE / "replay.lua"), PROBE_LOG=str(out / "probe.tsv"),
                       SHOT_FRAMES=",".join(map(str, shots)), LAST_FRAME=str(args.last))
    command = [str(MAME), args.game, "-bios", args.bios, "-noreadconfig", "-skip_gameinfo",
               "-rompath", f"{ROOT / 'private' / 'dumps' / args.game};{ROOT / 'private' / 'bios'}",
               "-cfg_directory", str(out / "cfg"), "-nvram_directory", str(out / "nvram"),
               "-snapshot_directory", str(out), "-video", "none", "-sound", "none", "-nothrottle",
               "-seconds_to_run", str(args.last // 59 + 60)]  # safety stop; the Lua script exits first
    if args.playback:
        lua = args.lua.resolve() if args.lua else HERE / "playback_shots.lua"
        command += ["-input_directory", str(args.playback.resolve().parent),
                    "-playback", args.playback.name, "-autoboot_script", str(lua)]
    else:
        script = parse(args.script.replace(";", "\n"))
        if args.session:
            transitions = continue_session(read_log(args.session.read_text()), args.cut, script)
        else:
            transitions = script.transitions()
        write_transitions(out / "transitions.tsv", transitions)
        (out / "shots.tsv").write_text("".join(f"{s}\tf{s:05d}.png\n" for s in shots))
        environment.update(REPLAY_TRANSITIONS=str(out / "transitions.tsv"),
                           REPLAY_SHOTS=str(out / "shots.tsv"))
        lua = args.lua.resolve() if args.lua else HERE / ("probe.lua" if args.probe else "replay.lua")
        command += ["-autoboot_script", str(lua)]
    with (out / "mame.log").open("w") as log:
        subprocess.run(command, cwd=MAME.parent, env=environment, stdout=log,
                       stderr=subprocess.STDOUT, check=True)
    print(out)


if __name__ == "__main__":
    main()
