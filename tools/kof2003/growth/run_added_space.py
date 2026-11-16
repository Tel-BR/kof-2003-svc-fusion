"""Run build C and build B on one script and check the Added Space tile (ticket 04).

    py -3 -m growth.run_added_space [--candidate build-c] [--reference build-b] [--script ...]

Build C is run against the ROM folder that holds the synthetic pair, build B against
the real one, with captures at the same frames. Every captured frame is then checked:
the tile must be in C's capture and in none of B's. Runs and captures go under
private/work/graphics-growth/runs/; only frame numbers, hashes and counts are printed.
Exit code 1 means the tile was missing from C, or present in B.
"""
import argparse
import sys
from datetime import datetime
from pathlib import Path

from growth.added_space_tiles import DEFAULT_ROM_DIR
from growth.verify_added_space import proof_constants, verify
from match.compare_captures import hash_set
from match.input_script import parse
from match.repeat_reference import GROWTH, SCRIPTS
from match.run import run_native, shot_name

# Attract mode and team selection: the screens are busy, so a tile drawn over them is
# a tile the renderer really fetched from the Added Space. Every captured frame has to
# be past PROOF_FIRST_FRAME, before which the planter leaves the booting board alone.
PLAN = {"frames": 4100, "shots": [2000, 3000, 4000]}


def run_both(script, candidate, reference, out, rom_dir, plan=PLAN, runs=run_native):
    parse(script.read_text())  # fail early on a malformed script
    first = proof_constants()["PROOF_FIRST_FRAME"]
    too_early = [frame for frame in plan["shots"] if frame <= first]
    if too_early:
        raise ValueError(f"frames {too_early} are at or before frame {first}, where the planter "
                         f"leaves the board alone; nothing would be drawn to find")
    args = (script.resolve(), plan["frames"], plan["shots"])
    reports = (runs(*args, out / "candidate", candidate / "KOF 2003.exe", rom_path=rom_dir),
               runs(*args, out / "reference", reference / "KOF 2003.exe"))
    results = {}
    for frame in plan["shots"]:
        results[frame] = verify(out / "candidate" / shot_name(frame),
                                out / "reference" / shot_name(frame))
    return results, reports


def failures(results, reports):
    """Everything that makes this run no proof at all, one line each."""
    out = []
    for frame, result in sorted(results.items()):
        if not result.matched:
            out.append(f"frame {frame}: the candidate does not show the tile "
                       f"({result.wrong_pixels} of 256 pixels differ)")
        if result.reference_matched:
            out.append(f"frame {frame}: the reference shows the tile too, so it proves nothing")
    for name, report in zip(("candidate", "reference"), reports):
        if report.mismatches:
            out.append(f"{name}: {report.mismatches} state mismatches in --verify")
    return out


def main(argv=None):
    options = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    options.add_argument("--candidate", type=lambda p: GROWTH / p, default=GROWTH / "build-c")
    options.add_argument("--reference", type=lambda p: GROWTH / p, default=GROWTH / "build-b")
    options.add_argument("--rom-dir", type=Path, default=DEFAULT_ROM_DIR)
    options.add_argument("--script", default="coin-start")
    args = options.parse_args(argv)
    for build in (args.candidate, args.reference):
        if not (build / "KOF 2003.exe").exists():
            raise SystemExit(f"{build / 'KOF 2003.exe'} not found")
    script = SCRIPTS / f"{args.script}.txt"
    out = GROWTH / "runs" / f"added-space-{args.script}-{datetime.now():%Y%m%d-%H%M%S}"
    results, reports = run_both(script, args.candidate, args.reference, out, args.rom_dir)
    for name, report in zip(("candidate", "reference"), reports):
        print(f"{name}: {report.blocks_checked} blocks, {report.mismatches} mismatches")
    digests = {name: hash_set(out / name) for name in ("candidate", "reference")}
    for frame, result in sorted(results.items()):
        print(f"frame {frame}: candidate {'shows the tile' if result.matched else 'NO tile'} at "
              f"{result.at} ({result.wrong_pixels} of 256 pixels differ); reference "
              f"{'SHOWS IT TOO' if result.reference_matched else 'does not'}")
        print(f"  candidate sha256 {digests['candidate'][frame]}")
        print(f"  reference sha256 {digests['reference'][frame]}")
    wrong = failures(results, reports)
    for line in wrong:
        print(line)
    print(f"captures: {out}")
    return 1 if wrong else 0


if __name__ == "__main__":
    sys.exit(main())
