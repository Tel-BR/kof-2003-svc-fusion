"""Synthetic tiles for the Added Space proof (graphics-set growth, ticket 04).

A small pair of graphics files whose tiles are a made-up pattern, not game art. In
build C the pair is listed as the fifth pair of the descriptor, so its first tile is
tile number $80000. Nothing here contains game data.

    py -3 -m growth.added_space_tiles [--pair-dir DIR] [--rom-dir DIR]

writes the pair under private/work/graphics-growth/synthetic/ and builds
private/work/graphics-growth/rom-c/, a ROM folder that links every file of the real
ROM folder and adds the pair. Builds A and B never see that folder.
"""
import argparse
import os
import shutil
import sys
from pathlib import Path

from match.repeat_reference import GROWTH

DEFAULT_PAIR_DIR = GROWTH / "synthetic"
DEFAULT_ROM_DIR = GROWTH / "rom-c"
FILE_NAMES = ("zz-synthetic-added-space.c9", "zz-synthetic-added-space.c10")
TILE_COUNT = 16
FIRST_TILE = 0x80000  # the fifth pair starts here: four pairs fill exactly 64 MiB


def tile_pixels(index):
    """The 256 colour indices (row by row) of synthetic tile `index`.

    Index 0 is transparent, so the pattern never uses it. The diagonal stripes are
    not symmetric: a horizontal or vertical flip would show.
    """
    slope = 1 + index // 4
    return [1 + (x + slope * y + index) % 15 for y in range(16) for x in range(16)]


def ng_colour(i):
    """The 16-bit Neo Geo palette word of entry i (1..15) of the proof palette.

    A word holds four high bits per gun (red at 11-8, green at 7-4, blue at 3-0), one
    extra low bit per gun at 14-12, and a "dark" bit at 15. The proof palette uses the
    high nibbles only, so the three guns walk apart as i grows and no two entries
    repeat. `added_space_proof.c` writes the same words from the same formula.
    """
    return ((i & 0xF) << 8) | (((15 - i) & 0xF) << 4) | ((7 * i) % 16)


def argb(word):
    """The colour the renderer shows for `word` (video.c, color_to_argb)."""
    dark = (word >> 15) & 1
    guns = (((word >> 7) & 0x1E) | ((word >> 14) & 1),
            ((word >> 3) & 0x1E) | ((word >> 13) & 1),
            ((word << 1) & 0x1E) | ((word >> 12) & 1))
    out = 0
    for gun in guns:
        out = (out << 8) | (((gun << 1) | (0 if dark else 1)) * 255 // 63)
    return 0xFF000000 | out


def tile_argb(index):
    """Tile `index` as the 256 ARGB pixels a capture should show, row by row."""
    return [argb(ng_colour(value)) for value in tile_pixels(index)]


def encode_tile(pixels):
    """The 128 bytes of paired tile data the renderer decodes into `pixels`."""
    data = bytearray(128)
    for y in range(16):
        for x in range(16):
            value = pixels[y * 16 + x]
            base = (0x40 if x < 8 else 0) + y * 4
            bit = 1 << (x % 8)
            for plane, offset in ((0, 0), (1, 2), (2, 1), (3, 3)):
                if value >> plane & 1:
                    data[base + offset] |= bit
    return bytes(data)


def decode_tile(data):
    """The inverse of `encode_tile`, following the renderer's decoding rule."""
    pixels = []
    for y in range(16):
        for x in range(16):
            base = (0x40 if x < 8 else 0) + y * 4
            bit = x % 8
            pixels.append(((data[base + 3] >> bit & 1) << 3) | ((data[base + 1] >> bit & 1) << 2)
                          | ((data[base + 2] >> bit & 1) << 1) | (data[base] >> bit & 1))
    return pixels


def encode_pair():
    """The two files of the pair: the even bytes of the tile data, and the odd ones."""
    tiles = b"".join(encode_tile(tile_pixels(i)) for i in range(TILE_COUNT))
    return tiles[0::2], tiles[1::2]


def write_pair(directory):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    for name, content in zip(FILE_NAMES, encode_pair()):
        (directory / name).write_bytes(content)
    return FILE_NAMES


def _link(source, target):
    try:
        os.link(source, target)
    except OSError:  # another drive, or a file system without hard links
        shutil.copyfile(source, target)


def prepare_rom_dir(source, pair_dir, target):
    """Make `target` hold every file of `source` (hard links) plus the synthetic pair.

    `target` is the folder build C is run against, and this owns it: anything else in
    it is deleted. So it must be a folder of its own. Aimed at the ROM folder it links
    from, it would delete the dumps it is supposed to link, which is why that is
    refused rather than guarded against halfway through.
    """
    source, pair_dir = Path(source).resolve(), Path(pair_dir).resolve()
    target = Path(target).resolve()
    if target in (source, pair_dir):
        raise ValueError(f"{target} is the folder this links from; the ROM folder for build C "
                         f"has to be a folder of its own, because it deletes whatever else is "
                         f"in it")
    target.mkdir(parents=True, exist_ok=True)
    wanted = {path.name: path for path in source.iterdir() if path.is_file()}
    for name in FILE_NAMES:
        wanted[name] = pair_dir / name
    for path in target.iterdir():
        if path.name not in wanted:
            path.unlink()
    for name, origin in wanted.items():
        destination = target / name
        if destination.exists():
            if destination.samefile(origin):
                continue      # already the same file; relinking it would be a needless unlink
            destination.unlink()
        _link(origin, destination)


def main(argv=None):
    # Imported here, not at the top: reading the native build's CMake cache is only
    # needed for the ROM folder, and the rest of this file is pure data.
    from match.run import cached_path

    options = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    options.add_argument("--pair-dir", type=Path, default=DEFAULT_PAIR_DIR)
    options.add_argument("--rom-dir", type=Path, default=DEFAULT_ROM_DIR)
    args = options.parse_args(argv)
    write_pair(args.pair_dir)
    prepare_rom_dir(cached_path("KOF2003_ROMS"), args.pair_dir, args.rom_dir)
    print(f"pair written to {args.pair_dir}; ROM folder for build C: {args.rom_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
