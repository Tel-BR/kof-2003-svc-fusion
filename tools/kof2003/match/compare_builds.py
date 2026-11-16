"""Run two builds on the same scripts and compare their captures by hash.

Used for graphics-set growth ticket 02: build A (64 MiB reference) against build B
(128 MiB, nothing else changed).

    py -3 -m match.compare_builds [--reference DIR] [--candidate DIR] [--scripts ...]

Each build is run once per script, headless, with the captures of
`repeat_reference.PLANS`. The candidate's memory use is measured on every run and
printed next to the machine's installed memory. Runs go under
private/work/graphics-growth/runs/. Captures hold game graphics: only hashes, frame
numbers and counts leave that folder. Exit code 1 means a difference, a missing
build, or a `--verify` summary worse than the reference's.
"""
import argparse
import sys
from datetime import datetime

from match.compare_captures import compare, hash_set
from match.input_script import parse
from match.memory_probe import MIB, run_measured, total_physical_memory
from match.repeat_reference import GROWTH, PLANS, SCRIPTS
from match.run import run_native


def compare_one(name, reference_dir, candidate_dir, out, measure=None, runs=run_native):
    """Run both builds on script `name`. Returns (comparison, ref_report, cand_report, memory)."""
    plan, script = PLANS[name], SCRIPTS / f"{name}.txt"
    parse(script.read_text())  # fail early on a malformed script
    args = (script.resolve(), plan["frames"], plan["shots"])
    ref = runs(*args, out / "reference", reference_dir / "KOF 2003.exe")
    memory = []
    runner = None
    if measure:
        def runner(command, stream):
            memory.append(measure(command, stream))
    cand = runs(*args, out / "candidate", candidate_dir / "KOF 2003.exe",
                **({"runner": runner} if runner else {}))
    return compare(out / "reference", out / "candidate"), ref, cand, memory


def worse(candidate, reference):
    """True when the candidate's --verify summary is worse than the reference's.

    Counts of blocks checked and instructions run may differ a little between runs of
    the same script, so only the failure counts decide: state mismatches, cycle-count
    differences and uncovered entry points.
    """
    return (candidate.mismatches > reference.mismatches
            or candidate.cycle_differences > reference.cycle_differences
            or candidate.uncovered_entry_points > reference.uncovered_entry_points)


def main(argv=None):
    options = argparse.ArgumentParser()
    options.add_argument("--reference", type=lambda p: GROWTH / p, default=GROWTH / "build-a")
    options.add_argument("--candidate", type=lambda p: GROWTH / p, default=GROWTH / "build-b")
    options.add_argument("--scripts", nargs="+", default=list(PLANS), choices=list(PLANS))
    args = options.parse_args(argv)
    for build in (args.reference, args.candidate):
        if not (build / "KOF 2003.exe").exists():
            raise SystemExit(f"{build / 'KOF 2003.exe'} not found")
    stamp = f"{datetime.now():%Y%m%d-%H%M%S}"
    print(f"installed memory: {total_physical_memory() // MIB} MiB")
    failed = False
    for name in args.scripts:
        out = GROWTH / "runs" / f"{args.reference.name}-vs-{args.candidate.name}-{name}-{stamp}"
        result, ref, cand, memory = compare_one(name, args.reference, args.candidate, out,
                                                measure=run_measured)
        print(f"{name}: reference {ref.blocks_checked} blocks, {ref.mismatches} mismatches; "
              f"candidate {cand.blocks_checked} blocks, {cand.mismatches} mismatches")
        for report in memory:
            print(f"{name}: candidate memory peak working set {report.peak_working_set // MIB} MiB, "
                  f"peak commit {report.peak_commit // MIB} MiB, "
                  f"steady working set {report.steady_working_set // MIB} MiB "
                  f"({report.samples} samples)")
        if worse(cand, ref):
            failed = True
            print(f"{name}: candidate --verify is WORSE than the reference "
                  f"(cycle differences {cand.cycle_differences} vs {ref.cycle_differences}, "
                  f"uncovered entry points {cand.uncovered_entry_points} vs "
                  f"{ref.uncovered_entry_points}, interpreted instructions "
                  f"{cand.interpreted_instructions} vs {ref.interpreted_instructions})")
        if result.equal:
            print(f"{name}: equal, {result.frames_compared} captures identical")
            for frame, digest in sorted(hash_set(out / "reference").items()):
                print(f"  frame {frame}: {digest}")
        else:
            failed = True
            frame, kind = result.first_difference
            print(f"{name}: NOT equal, first difference at frame {frame} ({kind}); see {out}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
