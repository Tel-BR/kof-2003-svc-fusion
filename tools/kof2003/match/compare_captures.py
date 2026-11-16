"""Compare two capture sets by hash and report equal or the first differing frame.

    py -3 -m match.compare_captures FIRST_DIR SECOND_DIR

Captures are the `frame-NNNNN.png` files the scripted native run writes. They
hold game graphics, so they stay under `private/`; only the hashes, frame
numbers and counts this step prints may go into tickets. Exit code 0 means
equal, 1 means a difference was found.
"""
import argparse
import hashlib
import re
import sys
from dataclasses import dataclass
from pathlib import Path

CAPTURE = re.compile(r"^frame-(\d+)\.png$")


@dataclass(frozen=True)
class Comparison:
    equal: bool
    first_difference: tuple  # (frame, "differs" | "missing in first" | "missing in second") or None
    frames_compared: int


def hash_set(directory):
    """SHA-256 of every capture in `directory`, keyed by frame number."""
    hashes = {}
    for path in Path(directory).iterdir():
        match = CAPTURE.match(path.name)
        if match:
            hashes[int(match.group(1))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def compare(first, second):
    a, b = hash_set(first), hash_set(second)
    frames = sorted(a.keys() | b.keys())
    if not frames:
        raise ValueError("no captures in either set; an empty comparison proves nothing")
    for frame in frames:
        if frame not in b:
            return Comparison(False, (frame, "missing in second"), len(frames))
        if frame not in a:
            return Comparison(False, (frame, "missing in first"), len(frames))
        if a[frame] != b[frame]:
            return Comparison(False, (frame, "differs"), len(frames))
    return Comparison(True, None, len(frames))


def main(argv=None):
    options = argparse.ArgumentParser()
    options.add_argument("first", type=Path)
    options.add_argument("second", type=Path)
    args = options.parse_args(argv)
    result = compare(args.first, args.second)
    if result.equal:
        print(f"equal: {result.frames_compared} captures identical")
        return 0
    frame, kind = result.first_difference
    print(f"first difference at frame {frame}: {kind} ({result.frames_compared} frames in the union)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
