"""Turn the private descriptor and renderer into build C, and back again.

Build C is the throwaway build that proves a tile above $80000 is loaded and drawn
(graphics-set growth, ticket 04). It needs three changes to the third-party copies
under private/, which this script makes repeatably and can undo. It copies none of
their code: it changes one value, inserts one pair of file names, and inserts a call
guarded by the KOF2003_ADDED_SPACE_PROOF macro.

    py -3 -m growth.added_space_patch status
    py -3 -m growth.added_space_patch apply    # build C
    py -3 -m growth.added_space_patch undo     # back to the descriptor A and B share

In the descriptor it raises the graphics size to 128 MiB (as `growth.graphics_size`
does) and adds the synthetic pair of `growth.added_space_tiles` as the fifth pair, so
its first tile is tile number $80000. In the renderer it inserts, at the top of
video_render_line(), a call to kof2003_plant_added_space_sprite(), which
`growth/added_space_proof.c` defines; without the macro that call is not compiled, so
a renderer carrying the insertion still builds A and B unchanged.

Both files are checked before either is written, so a refusal leaves both alone. Each
command prints the SHA-256 of both files before and after.
"""
import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from growth.added_space_tiles import FILE_NAMES, FIRST_TILE
from growth.graphics_size import (DEFAULT_DESCRIPTOR, MIB_128, MIB_64, read_size, set_size,
                                  sha256, write_atomically)

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_RENDERER = (ROOT / "private" / "work" / "samsho-runtime-source" / "neogeorecomp"
                    / "src" / "video.c")
MACRO = "KOF2003_ADDED_SPACE_PROOF"
BEGIN = f"/* {MACRO} begin (tools/kof2003/growth/added_space_patch.py) */"
END = f"/* {MACRO} end */"
# The four original pairs fill exactly 64 MiB, so the synthetic pair is the fifth and
# its first tile is tile number $80000, which added_space_tiles.FIRST_TILE assumes. A
# descriptor with any other number of pairs would put it somewhere else, and the
# loader lays out at most NG_MAX_PARTS = 8 pairs in any case.
PAIRS_BEFORE_ADDED_SPACE = 4

# The pair list, and the first line of video_render_line()'s body. Both name only what
# they have to find; neither carries any of the code they are matched against.
_PAIRS = re.compile(rb"(\.crom_pairs\s*=\s*\{)(.*?)(\r?\n[ \t]*\},)", re.DOTALL)
_ONE_PAIR = re.compile(rb"\{\s*\"")
_RENDER_LINE = re.compile(rb"^[\w \t\*]*\bvideo_render_line\s*\([^)]*\)\s*\{", re.MULTILINE)
# An inserted block, with the line break and indent that precede it: removing exactly
# that gives the original bytes back.
_BLOCK = re.compile(rb"\r?\n[ \t]*" + re.escape(BEGIN.encode()) + rb".*?"
                    + re.escape(END.encode()), re.DOTALL)


@dataclass(frozen=True)
class State:
    descriptor: bool   # the pair is in the descriptor
    renderer: bool     # the call is in the renderer
    size: int          # the graphics size the descriptor asks for


def _insert(data, cut, lines, indent):
    """`data` with `lines` put in at offset `cut`, as its own indented block.

    The line break of the original line at `cut` is kept where it was, so removing the
    block with _BLOCK gives the original bytes back. Preprocessor lines stay at column
    zero; everything else takes `indent`.
    """
    crlf = b"\r\n" in data
    text = "".join(f"{'' if line.startswith('#') else indent}{line}\n" for line in lines)
    block = (text.replace("\n", "\r\n") if crlf else text).encode().rstrip(b"\r\n")
    return data[:cut] + (b"\r\n" if crlf else b"\n") + block + data[cut:]


def _add_pair(data):
    """`data` with the synthetic pair added as the last pair of the list."""
    found = _PAIRS.search(data)
    if not found:
        raise ValueError("no .crom_pairs list in the descriptor")
    pairs = len(_ONE_PAIR.findall(found.group(2)))
    if pairs != PAIRS_BEFORE_ADDED_SPACE:
        raise ValueError(f"the descriptor lists {pairs} pairs, not {PAIRS_BEFORE_ADDED_SPACE}: "
                         f"the Added Space starts at the fifth pair, so a fifth pair added here "
                         f"would not begin at tile 0x{FIRST_TILE:X}")
    names = ", ".join(f'"{name}"' for name in FILE_NAMES)
    return _insert(data, found.end(2), [BEGIN, f"{{{names}}},", END], " " * 8)


def _add_hook(data):
    """`data` with the planting call inserted at the top of video_render_line()."""
    found = _RENDER_LINE.search(data)
    if not found:
        raise ValueError("no video_render_line() in the renderer")
    return _insert(data, found.end(), [BEGIN,
                                       f"#ifdef {MACRO}",
                                       "void kof2003_plant_added_space_sprite(void);",
                                       "kof2003_plant_added_space_sprite();",
                                       "#endif",
                                       END], " " * 4)


def first_pair(descriptor=DEFAULT_DESCRIPTOR):
    """The file names of the descriptor's first graphics pair, i.e. where tile 0 lives."""
    found = _PAIRS.search(Path(descriptor).read_bytes())
    if not found:
        raise ValueError("no .crom_pairs list in the descriptor")
    names = re.findall(rb"\"([^\"]+)\"", found.group(2))
    if len(names) < 2:
        raise ValueError("the descriptor's first pair does not name two files")
    return names[0].decode(), names[1].decode()


def state(descriptor=DEFAULT_DESCRIPTOR, renderer=DEFAULT_RENDERER):
    return State(BEGIN.encode() in Path(descriptor).read_bytes(),
                 BEGIN.encode() in Path(renderer).read_bytes(),
                 read_size(descriptor))


def apply(descriptor=DEFAULT_DESCRIPTOR, renderer=DEFAULT_RENDERER):
    """Make both files build C. Returns False if they already do."""
    descriptor, renderer = Path(descriptor), Path(renderer)
    was = state(descriptor, renderer)
    if was == State(True, True, MIB_128):
        return False
    new_descriptor = descriptor.read_bytes() if was.descriptor else _add_pair(descriptor.read_bytes())
    new_renderer = renderer.read_bytes() if was.renderer else _add_hook(renderer.read_bytes())
    new_descriptor = set_size(new_descriptor, MIB_64, MIB_128) or new_descriptor
    write_atomically(descriptor, new_descriptor)
    write_atomically(renderer, new_renderer)
    return True


def undo(descriptor=DEFAULT_DESCRIPTOR, renderer=DEFAULT_RENDERER):
    """Take build C back out of both files. Returns False if it was not there."""
    descriptor, renderer = Path(descriptor), Path(renderer)
    was = state(descriptor, renderer)
    if was == State(False, False, MIB_64):
        return False
    new_descriptor = _BLOCK.sub(b"", descriptor.read_bytes())
    new_descriptor = set_size(new_descriptor, MIB_128, MIB_64) or new_descriptor
    write_atomically(descriptor, new_descriptor)
    write_atomically(renderer, _BLOCK.sub(b"", renderer.read_bytes()))
    return True


def _report(when, descriptor, renderer):
    now = state(descriptor, renderer)
    print(f"{when}: graphics size 0x{now.size:X}, pair in the descriptor "
          f"{'yes' if now.descriptor else 'no'}, call in the renderer "
          f"{'yes' if now.renderer else 'no'}")
    print(f"  descriptor sha256 {sha256(descriptor)}")
    print(f"  renderer   sha256 {sha256(renderer)}")


def main(argv=None):
    options = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    options.add_argument("command", choices=["status", "apply", "undo"])
    options.add_argument("--descriptor", type=Path, default=DEFAULT_DESCRIPTOR)
    options.add_argument("--renderer", type=Path, default=DEFAULT_RENDERER)
    args = options.parse_args(argv)
    for path in (args.descriptor, args.renderer):
        if not path.is_file():
            raise SystemExit(f"{path} not found")
    _report("before", args.descriptor, args.renderer)
    if args.command != "status":
        try:
            changed = (apply if args.command == "apply" else undo)(args.descriptor, args.renderer)
        except ValueError as problem:
            raise SystemExit(f"error: {problem}")
        _report("after ", args.descriptor, args.renderer)
        if not changed:
            print("already in that state, nothing written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
