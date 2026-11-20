"""Probe the same memory each frame in the native player and in MAME, then compare (ticket 08).

    py -3 -m match.probe_run SCRIPT --frames N [--probe SPEC] [--shift S] [--first F] [--last L]
                             [--player EXE] [--rom-path DIR] [--verify] [--only native|mame]

Both runs are silent and start from power-on. The native player must be built with the CMake
option KOF2003_NATIVE_PROBE (see README.md); it logs through KOF_NATIVE_PROBE and
KOF_NATIVE_PROBE_LOG. MAME logs through probe.lua's PROBE_ADDRESSES with REPLAY_OFFSET 2, so
both logs carry the native player's frame numbers. --shift compares native frame N with MAME
frame N + S. The default addresses are TEAM_MATCH_ADDRESSES. Output goes to
private/work/native-probe/runs/<script>-<time>/; exit code 1 means the logs differ.
"""
import argparse
import sys
from datetime import datetime
from pathlib import Path

from match.input_script import parse
from match.probe_log import compare, describe, format_spec, parse_spec, read_log
from match.run import WORK, cached_path, run_mame, run_native

HERE = Path(__file__).resolve().parent
PROBE_LUA = HERE / "probe.lua"
REPLAY_LUA = HERE / "replay.lua"
PLAYER = WORK / "native-probe" / "build" / "KOF 2003.exe"
RUNS = WORK / "native-probe" / "runs"
MAME_OFFSET = "2"  # replay.lua's measured alignment for kof2003 with the Europe MVS v2 BIOS

# P1's first fighter object ($101080) pose pointer at +$60, then P1's and P2's health for team
# members 1-3, kept in NEO-PVC RAM (ticket 08).
TEAM_MATCH_ADDRESSES = ("0x1010e0:4,0x2fe91d:1,0x2fea1d:1,0x2feb1d:1,"
             "0x2fed1d:1,0x2fee1d:1,0x2fef1d:1")


def probe(script_path, frames, spec, out, player=PLAYER, rom_path=None, shift=0, first=None,
          last=None, verify=False, only=None, native_runner=None, mame_runner=run_mame):
    """Run what `only` allows and return the comparison (None when only one side ran)."""
    probes = parse_spec(spec)
    spec = format_spec(probes)
    script = parse(Path(script_path).read_text())
    native_log, mame_log = out / "native" / "probe.tsv", out / "mame" / "probe.tsv"
    if only != "mame":
        runner = {"runner": native_runner} if native_runner else {}
        report = run_native(Path(script_path).resolve(), frames, [], out / "native", player=player,
                            rom_path=rom_path, verify=verify, **runner,
                            environment={"KOF_NATIVE_PROBE": spec, "KOF_NATIVE_PROBE_LOG": str(native_log)})
        if report:
            print(report)
        if not native_log.exists():
            raise RuntimeError(f"{player} wrote no probe log; build it with KOF2003_NATIVE_PROBE=ON")
    if only != "native":
        mame_runner(script, frames, [], out / "mame", lua=PROBE_LUA,
                    environment={"REPLAY_LUA": str(REPLAY_LUA), "REPLAY_OFFSET": MAME_OFFSET,
                                 "PROBE_ADDRESSES": spec, "PROBE_LOG": str(mame_log)})
    if only:
        return None
    return compare(read_log(native_log.read_text(), len(probes)),
                   read_log(mame_log.read_text(), len(probes)), shift, first, last)


def main(argv=None):
    options = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    options.add_argument("script", type=Path)
    options.add_argument("--frames", type=int, required=True)
    options.add_argument("--probe", default=TEAM_MATCH_ADDRESSES)
    options.add_argument("--shift", type=int, default=0)
    options.add_argument("--first", type=int)
    options.add_argument("--last", type=int)
    options.add_argument("--player", type=Path, default=PLAYER)
    options.add_argument("--rom-path", type=Path)
    options.add_argument("--verify", action="store_true")
    options.add_argument("--only", choices=["native", "mame"])
    args = options.parse_args(argv)
    out = RUNS / f"{args.script.stem}-{datetime.now():%Y%m%d-%H%M%S}"
    result = probe(args.script, args.frames, args.probe, out, args.player,
                   args.rom_path or cached_path("KOF2003_ROMS"), args.shift, args.first, args.last,
                   args.verify, args.only)
    print(out)
    if result is None:
        return 0
    summary = describe(result, args.shift)
    (out / "summary.txt").write_text(summary + "\n")
    print(summary)
    return 0 if result.equal else 1


if __name__ == "__main__":
    sys.exit(main())
