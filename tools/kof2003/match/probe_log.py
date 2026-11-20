"""Per-frame memory probe logs, shared by the native player and MAME (ticket 08).

Both runtimes take the same address list, "ADDRESS:SIZE[,ADDRESS:SIZE...]", with each
address in hex (68000 bus, for example work RAM at $100000 or NEO-PVC RAM at $2FE000)
and SIZE 1, 2 or 4 bytes. Both write one line per frame:
"<frame>\t<value>\t<value>...", each value in lowercase hex, two digits per byte.
The native player takes the list in KOF_NATIVE_PROBE and the log path in
KOF_NATIVE_PROBE_LOG; probe.lua takes PROBE_ADDRESSES and PROBE_LOG.

    py -3 -m match.probe_log NATIVE_LOG MAME_LOG --columns N [--shift S] [--first F] [--last L]

compares two logs and prints the first difference; exit code 1 means they differ.
Logs hold game memory: keep them under private/.
"""
import argparse
import re
import sys
from dataclasses import dataclass, field

SIZES = (1, 2, 4)
MAX_PROBES = 16  # PROBE_MAX in native_probe.c
ENTRY = re.compile(r"\s*0x([0-9a-fA-F]{1,6}):([0-9])\s*")


@dataclass(frozen=True)
class Probe:
    address: int
    size: int


def parse_spec(text):
    probes = []
    for number, item in enumerate(text.split(","), start=1):
        match = ENTRY.fullmatch(item)
        if not match:
            raise ValueError(f"entry {number}: expected 0xADDRESS:SIZE, got {item!r}")
        address, size = int(match[1], 16), int(match[2])
        if size not in SIZES:
            raise ValueError(f"entry {number}: size must be 1, 2 or 4")
        if size > 1 and address % 2:
            raise ValueError(f"entry {number}: a {size}-byte read needs an even address")
        probes.append(Probe(address, size))
    if len(probes) > MAX_PROBES:
        raise ValueError(f"at most {MAX_PROBES} addresses per run")
    return tuple(probes)


def format_spec(probes):
    return ",".join(f"0x{p.address:06x}:{p.size}" for p in probes)


def read_log(text, columns):
    log = {}
    for number, line in enumerate(text.splitlines(), start=1):
        if not line:
            continue
        fields = line.split("\t")
        if len(fields) != columns + 1:
            raise ValueError(f"line {number}: expected {columns} values")
        log[int(fields[0])] = tuple(fields[1:])
    return log


@dataclass(frozen=True)
class Mismatch:
    frame: int  # left frame; the right frame is frame + shift
    column: int
    left: str
    right: str


@dataclass(frozen=True)
class Comparison:
    frames: int  # frames present on both sides inside the window
    missing: int  # frames inside the window present on one side only
    mismatched_frames: int
    first: Mismatch = None
    first_by_column: dict = field(default_factory=dict)

    @property
    def equal(self):
        return self.frames > 0 and self.first is None


def compare(left, right, shift=0, first=None, last=None):
    """Compare left frame N with right frame N + shift over left frames [first, last]."""
    def inside(frame):
        return (first is None or frame >= first) and (last is None or frame <= last)

    wanted = {f for f in left if inside(f)} | {f - shift for f in right if inside(f - shift)}
    frames = missing = mismatched = 0
    earliest, by_column = None, {}
    for frame in sorted(wanted):
        if frame not in left or frame + shift not in right:
            missing += 1
            continue
        frames += 1
        a, b = left[frame], right[frame + shift]
        differing = [c for c in range(max(len(a), len(b))) if a[c:c + 1] != b[c:c + 1]]
        if differing:
            mismatched += 1
            for column in differing:
                by_column.setdefault(column, frame)
            if earliest is None:
                c = differing[0]
                earliest = Mismatch(frame, c, a[c] if c < len(a) else "", b[c] if c < len(b) else "")
    return Comparison(frames, missing, mismatched, earliest, by_column)


def describe(result, shift=0):
    if result.equal:
        return f"equal on {result.frames} frames ({result.missing} on one side only)"
    if result.frames == 0:
        return "no frame present in both logs"
    m = result.first
    columns = ", ".join(f"column {c} from frame {f}" for c, f in sorted(result.first_by_column.items()))
    return (f"{result.mismatched_frames} of {result.frames} frames differ; first at frame {m.frame} "
            f"(right frame {m.frame + shift}), column {m.column}: {m.left} vs {m.right}; {columns}")


def main(argv=None):
    options = argparse.ArgumentParser(description="Compare two probe logs.")
    options.add_argument("left", type=argparse.FileType("r"))
    options.add_argument("right", type=argparse.FileType("r"))
    options.add_argument("--columns", type=int, required=True)
    options.add_argument("--shift", type=int, default=0)
    options.add_argument("--first", type=int)
    options.add_argument("--last", type=int)
    args = options.parse_args(argv)
    result = compare(read_log(args.left.read(), args.columns), read_log(args.right.read(), args.columns),
                     args.shift, args.first, args.last)
    print(describe(result, args.shift))
    return 0 if result.equal else 1


if __name__ == "__main__":
    sys.exit(main())
