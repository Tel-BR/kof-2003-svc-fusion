"""Raise or lower the graphics size in the private cartridge descriptor.

The descriptor is third-party code under private/. This script changes one value in it
and nothing else, repeatably and reversibly, and copies none of its code:

    py -3 -m growth.graphics_size status
    py -3 -m growth.graphics_size apply     # 64 MiB -> 128 MiB (build B)
    py -3 -m growth.graphics_size undo      # 128 MiB -> 64 MiB (build A)

Each command prints the file's SHA-256 before and after, so an apply followed by an
undo can be confirmed to give the original bytes back.
"""
import argparse
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DESCRIPTOR = ROOT / "private" / "work" / "kof2003-port" / "src" / "game.c"
MIB_64 = 0x4000000
MIB_128 = 0x8000000
_SIZE = re.compile(rb"(^[ \t]*\.crom_size[ \t]*=[ \t]*)(0[xX][0-9A-Fa-f]+)", re.MULTILINE)


def _find(data):
    found = list(_SIZE.finditer(data))
    if not found:
        raise ValueError("no .crom_size line in the descriptor")
    if len(found) > 1:
        raise ValueError(".crom_size appears more than once in the descriptor")
    return found[0]


def read_size(path):
    return int(_find(Path(path).read_bytes()).group(2), 16)


def _set(path, old, new):
    """Change the size from old to new. Returns False if it already is new."""
    path = Path(path)
    data = path.read_bytes()
    match = _find(data)
    current = int(match.group(2), 16)
    if current == new:
        return False
    if current != old:
        raise ValueError(f"the graphics size is {match.group(2).decode()}; "
                         f"expected 0x{old:X} or 0x{new:X}")
    literal = f"0x{new:X}".encode()
    changed = data[:match.start(2)] + literal + data[match.end(2):]
    scratch = path.with_name(path.name + ".tmp")
    scratch.write_bytes(changed)
    scratch.replace(path)
    return True


def apply(path):
    return _set(path, MIB_64, MIB_128)


def undo(path):
    return _set(path, MIB_128, MIB_64)


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _label(size):
    return f"{size // (1 << 20)} MiB" if size % (1 << 20) == 0 else f"{size} bytes"


def main(argv=None):
    options = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    options.add_argument("command", choices=["status", "apply", "undo"])
    options.add_argument("--descriptor", type=Path, default=DEFAULT_DESCRIPTOR)
    args = options.parse_args(argv)
    if not args.descriptor.is_file():
        raise SystemExit(f"{args.descriptor} not found")
    before_hash, before = sha256(args.descriptor), read_size(args.descriptor)
    print(f"before: 0x{before:X} ({_label(before)}) sha256 {before_hash}")
    if args.command != "status":
        try:
            changed = (apply if args.command == "apply" else undo)(args.descriptor)
        except ValueError as problem:
            raise SystemExit(f"error: {problem}")
        after_hash, after = sha256(args.descriptor), read_size(args.descriptor)
        note = "changed" if changed else "already in that state, nothing written"
        print(f"after:  0x{after:X} ({_label(after)}) sha256 {after_hash} [{note}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
