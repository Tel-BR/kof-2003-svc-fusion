"""Decide, from the captures, whether the Added Space tile was drawn (ticket 04).

    py -3 -m growth.verify_added_space CANDIDATE.png [REFERENCE.png] [--rom-path DIR]

The candidate is a capture of build C, the reference the same frame of build B (or of
C with the option off). The tile is expected where `added_space_proof.c` puts it: the
constants are read from that file, so there is one place to change. Every pixel of the
16x16 box is compared with the colours the synthetic tile must show, which is what
proves the tile was found at tile number $80000, decoded and drawn in its palette.

With --rom-path the first tile of the Graphics Set is read as well, and only the
SHA-256 of the two tiles' 128 bytes is printed, so what leaves `private/` is a hash.
Exit code 0 means the tile is in the candidate and not in the reference.
"""
import argparse
import hashlib
import re
import struct
import sys
import zlib
from dataclasses import dataclass
from pathlib import Path

from growth.added_space_patch import DEFAULT_DESCRIPTOR, first_pair
from growth.added_space_tiles import (FIRST_TILE, TILE_COUNT, encode_tile, tile_argb,
                                      tile_pixels)

PROOF_C = Path(__file__).with_name("added_space_proof.c")
NEEDED = ("PROOF_TILE", "PROOF_X", "PROOF_Y", "PROOF_FIRST_FRAME")
SCREEN_W, SCREEN_H = 320, 224
TILE_SIDE = 16


@dataclass(frozen=True)
class Image:
    width: int
    height: int
    pixels: list  # ARGB, row by row


@dataclass(frozen=True)
class Result:
    at: tuple               # where the tile is expected
    matched: bool           # the candidate shows exactly that tile there
    wrong_pixels: int       # how many of the 256 do not match
    reference_matched: bool = None  # the same box of the reference, if one was given


def proof_constants(path=PROOF_C):
    """The #define values of the proof's C file, as integers."""
    text = Path(path).read_text()
    found = {}
    for name in NEEDED:
        match = re.search(rf"^#define\s+{name}\s+(0[xX][0-9A-Fa-f]+|\d+)u?\b", text, re.MULTILINE)
        if not match:
            raise ValueError(f"{path} does not define {name}")
        found[name] = int(match.group(1), 0)
    return found


def _unfilter(raw, width, height):
    """Undo the PNG row filters of an 8-bit RGB image. Returns rows of bytes."""
    stride = width * 3
    rows, previous = [], bytes(stride)
    at = 0
    for _ in range(height):
        kind, line = raw[at], bytearray(raw[at + 1:at + 1 + stride])
        at += 1 + stride
        for i in range(stride):
            left = line[i - 3] if i >= 3 else 0
            up = previous[i]
            upleft = previous[i - 3] if i >= 3 else 0
            if kind == 0:
                continue
            if kind == 1:
                line[i] = (line[i] + left) & 0xFF
            elif kind == 2:
                line[i] = (line[i] + up) & 0xFF
            elif kind == 3:
                line[i] = (line[i] + (left + up) // 2) & 0xFF
            elif kind == 4:
                guess = left + up - upleft
                best = min((abs(guess - option), option) for option in (left, up, upleft))[1]
                line[i] = (line[i] + best) & 0xFF
            else:
                raise ValueError(f"unknown PNG row filter {kind}")
        rows.append(bytes(line))
        previous = rows[-1]
    return rows


def read_png(path):
    """An 8-bit RGB PNG as ARGB pixels. Enough for the captures the player writes."""
    data = Path(path).read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path} is not a PNG")
    at, head, idat = 8, None, b""
    while at + 8 <= len(data):
        length, kind = struct.unpack(">I", data[at:at + 4])[0], data[at + 4:at + 8]
        payload = data[at + 8:at + 8 + length]
        at += 12 + length
        if kind == b"IHDR":
            head = struct.unpack(">IIBBBBB", payload)
        elif kind == b"IDAT":
            idat += payload
        elif kind == b"IEND":
            break
    if not head:
        raise ValueError(f"{path} has no IHDR")
    width, height, depth, colour, compression, filtering, interlace = head
    if (depth, colour) != (8, 2) or interlace:
        raise ValueError(f"{path} is not a plain 8-bit RGB PNG (depth {depth}, "
                         f"colour type {colour}, interlace {interlace})")
    if compression or filtering:
        raise ValueError(f"{path} uses an unknown compression or filtering method")
    rows = _unfilter(zlib.decompress(idat), width, height)
    pixels = [0xFF000000 | (row[x * 3] << 16) | (row[x * 3 + 1] << 8) | row[x * 3 + 2]
              for row in rows for x in range(width)]
    return Image(width, height, pixels)


def box(image, x, y, side=TILE_SIDE):
    return [image.pixels[(y + row) * image.width + x + column]
            for row in range(side) for column in range(side)]


def _wrong(image, at, tile):
    expected = tile_argb(tile)
    return sum(1 for shown, want in zip(box(image, *at), expected) if shown != want)


def planted_tile(constants):
    """Which synthetic tile the C file plants, as an index into the pair."""
    index = constants["PROOF_TILE"] - FIRST_TILE
    if not 0 <= index < TILE_COUNT:
        raise ValueError(f"PROOF_TILE is 0x{constants['PROOF_TILE']:X}, which is not one of the "
                         f"{TILE_COUNT} synthetic tiles from 0x{FIRST_TILE:X}")
    return index


def verify(candidate, reference=None, tile=None, source=PROOF_C):
    constants = proof_constants(source)
    tile = planted_tile(constants) if tile is None else tile
    at = (constants["PROOF_X"], constants["PROOF_Y"])
    shown = read_png(candidate)
    if (shown.width, shown.height) != (SCREEN_W, SCREEN_H):
        raise ValueError(f"{candidate} is {shown.width}x{shown.height}, not {SCREEN_W}x{SCREEN_H}")
    wrong = _wrong(shown, at, tile)
    other = None
    if reference is not None:
        before = read_png(reference)
        if (before.width, before.height) != (SCREEN_W, SCREEN_H):
            raise ValueError(f"{reference} is {before.width}x{before.height}, "
                             f"not {SCREEN_W}x{SCREEN_H}")
        other = _wrong(before, at, tile) == 0
    return Result(at, wrong == 0, wrong, other)


def tile_digests(rom_path, descriptor=DEFAULT_DESCRIPTOR, tile=0):
    """SHA-256 of the synthetic tile's bytes and of the Graphics Set's first tile.

    The second reads 64 bytes from each file of the descriptor's first pair, which is
    game data: only the hash is returned, never the bytes.
    """
    rom_path = Path(rom_path)
    halves = [(rom_path / name).read_bytes()[:64] for name in first_pair(descriptor)]
    paired = bytes(byte for pair in zip(*halves) for byte in pair)
    return (hashlib.sha256(encode_tile(tile_pixels(tile))).hexdigest(),
            hashlib.sha256(paired).hexdigest())


def main(argv=None):
    options = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    options.add_argument("candidate", type=Path)
    options.add_argument("reference", type=Path, nargs="?")
    options.add_argument("--tile", type=int, help="override which synthetic tile to expect")
    options.add_argument("--rom-path", type=Path, help="also hash the Graphics Set's first tile")
    args = options.parse_args(argv)
    result = verify(args.candidate, args.reference, args.tile)
    tile = planted_tile(proof_constants()) if args.tile is None else args.tile
    where = f"the 16x16 box at {result.at}"
    print(f"candidate: {'the synthetic tile is there' if result.matched else 'NOT the tile'} in "
          f"{where} ({result.wrong_pixels} of 256 pixels differ from tile "
          f"{tile} at tile number 0x{FIRST_TILE + tile:X})")
    if result.reference_matched is not None:
        print(f"reference: {'the tile is THERE TOO' if result.reference_matched else 'no such tile'}"
              f" in {where}")
    if args.rom_path:
        synthetic, game = tile_digests(args.rom_path, tile=tile)
        print(f"synthetic tile sha256 {synthetic}")
        print(f"graphics set tile 0 sha256 {game}")
        print(f"the two tiles differ: {'yes' if synthetic != game else 'NO'}")
    return 0 if result.matched and not result.reference_matched else 1


if __name__ == "__main__":
    sys.exit(main())
