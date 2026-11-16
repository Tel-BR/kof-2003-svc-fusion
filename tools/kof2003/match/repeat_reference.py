"""Run one build twice on the same scripts and compare the captures by hash.

Used for graphics-set growth ticket 01 (the reference build must repeat itself)
and, with --build pointing at another build, for comparing builds later.

    py -3 -m match.repeat_reference [--build DIR] [--scripts coin-start team-match]

Everything is written under private/work/graphics-growth/. Captures hold game
graphics: only hashes, frame numbers and counts leave that folder.
"""
import argparse
import sys
from datetime import datetime
from pathlib import Path

from match.compare_captures import compare, hash_set
from match.input_script import parse
from match.run import WORK, run_native

SCRIPTS = Path(__file__).with_name("scripts")
GROWTH = WORK / "graphics-growth"
DEFAULT_BUILD = GROWTH / "build-a"
# Boot, attract mode, selection and the fight, as frames from power-on.
PLANS = {
    "coin-start": {"frames": 6000, "shots": [600, 2000, 3000, 4000, 5400]},
    "team-match": {"frames": 8000, "shots": [600, 2000, 3000, 4000, 5400, 6000, 7000]},
}


def main(argv=None):
    options = argparse.ArgumentParser()
    options.add_argument("--build", type=Path, default=DEFAULT_BUILD,
                         help="folder holding 'KOF 2003.exe' and SDL2.dll (default: build A)")
    options.add_argument("--scripts", nargs="+", default=list(PLANS), choices=list(PLANS))
    args = options.parse_args(argv)
    player = args.build / "KOF 2003.exe"
    if not player.exists():
        raise SystemExit(f"{player} not found")
    stamp = f"{datetime.now():%Y%m%d-%H%M%S}"
    failed = False
    for name in args.scripts:
        plan, script = PLANS[name], SCRIPTS / f"{name}.txt"
        parse(script.read_text())  # fail early on a malformed script
        out = GROWTH / "runs" / f"{args.build.name}-{name}-{stamp}"
        for run in ("run1", "run2"):
            report = run_native(script.resolve(), plan["frames"], plan["shots"], out / run, player)
            print(f"{name} {run}: {report.blocks_checked} blocks, {report.mismatches} mismatches")
        result = compare(out / "run1", out / "run2")
        hashes = hash_set(out / "run1")
        if result.equal:
            print(f"{name}: equal, {result.frames_compared} captures")
            for frame, digest in sorted(hashes.items()):
                print(f"  frame {frame}: {digest}")
        else:
            failed = True
            frame, kind = result.first_difference
            print(f"{name}: NOT equal, first difference at frame {frame} ({kind}); see {out}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
