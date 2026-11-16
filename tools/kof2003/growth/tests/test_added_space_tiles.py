"""The synthetic tiles for the Added Space proof: encoding, files and the ROM folder.

The tiles are a made-up pattern, not game art. Expected values are written out by hand
or computed from the decoding rule the player's renderer uses (video.c, decode_sprites):
byte j of a 128-byte tile holds, for the left half of row y (pixels 0-7) at 0x40 + 4y + n,
for the right half (pixels 8-15) at 4y + n, one bit plane of eight pixels, pixel x in
bit x. Plane 0 is byte 0, plane 1 is byte 2, plane 2 is byte 1, plane 3 is byte 3.
"""
from pathlib import Path

import pytest

from growth import added_space_tiles as tiles


def test_a_single_pixel_lands_in_the_byte_the_renderer_reads():
    # Pixel (x=0, y=0) with index 0b0101 (planes 0 and 2): left half, row 0.
    blank = [0] * 256
    pixels = list(blank)
    pixels[0] = 0b0101

    data = tiles.encode_tile(pixels)

    expected = bytearray(128)
    expected[0x40 + 0] = 0x01  # plane 0, bit x=0
    expected[0x40 + 1] = 0x01  # plane 2 sits in byte 1
    assert bytes(data) == bytes(expected)


def test_a_pixel_in_the_right_half_uses_the_first_half_of_the_tile():
    pixels = [0] * 256
    pixels[3 * 16 + 15] = 0b1000  # x=15, y=3: plane 3, right half, bit 7

    data = tiles.encode_tile(pixels)

    expected = bytearray(128)
    expected[3 * 4 + 3] = 0x80
    assert bytes(data) == bytes(expected)


def test_every_pattern_tile_survives_encode_then_decode():
    for index in range(tiles.TILE_COUNT):
        pixels = tiles.tile_pixels(index)
        assert tiles.decode_tile(tiles.encode_tile(pixels)) == pixels


def test_pattern_tiles_are_opaque_and_all_different():
    seen = set()
    for index in range(tiles.TILE_COUNT):
        pixels = tiles.tile_pixels(index)
        assert len(pixels) == 256
        assert 0 not in pixels, "index 0 is transparent; a hole could hide the tile"
        assert max(pixels) <= 15
        seen.add(tuple(pixels))
    assert len(seen) == tiles.TILE_COUNT


def test_the_pattern_is_not_symmetric_so_a_flip_would_show():
    pixels = tiles.tile_pixels(0)
    rows = [pixels[y * 16:(y + 1) * 16] for y in range(16)]
    assert rows != [row[::-1] for row in rows]
    assert rows != rows[::-1]


def test_the_pair_interleaves_back_into_the_tiles_in_order():
    first, second = tiles.encode_pair()

    assert len(first) == len(second) == tiles.TILE_COUNT * 64
    crom = bytearray()
    for a, b in zip(first, second):
        crom += bytes([a, b])
    for index in range(tiles.TILE_COUNT):
        chunk = bytes(crom[index * 128:(index + 1) * 128])
        assert tiles.decode_tile(chunk) == tiles.tile_pixels(index)


def test_palette_words_hold_the_nibbles_the_formula_says():
    assert tiles.ng_colour(1) == 0x01E7  # red 1, green 14, blue 7
    assert tiles.ng_colour(15) == 0x0F09  # red 15, green 0, blue 105 mod 16 = 9
    words = [tiles.ng_colour(i) for i in range(1, 16)]
    assert len(set(words)) == 15
    assert all(word & 0xF000 == 0 for word in words), "no dark bit and no extra low bits"


def test_argb_follows_the_renderer_on_words_computed_by_hand():
    # Every gun at full nibble, no extra low bit: 15*2 = 30, then (30<<1)|1 = 61 steps
    # of 63, so 61*255//63 = 246 = 0xF6.
    assert tiles.argb(0x0FFF) == 0xFFF6F6F6
    # All nibbles zero: one step of 63, 1*255//63 = 4.
    assert tiles.argb(0x0000) == 0xFF040404
    # The three extra low bits (14-12) with zero nibbles: 1, then 3 steps, 3*255//63 = 12.
    assert tiles.argb(0x7000) == 0xFF0C0C0C
    # The dark bit removes the lowest step from all three guns.
    assert tiles.argb(0x8000) == 0xFF000000


def test_every_proof_colour_is_opaque_and_distinct_on_screen():
    shown = [tiles.argb(tiles.ng_colour(i)) for i in range(1, 16)]
    assert len(set(shown)) == 15
    assert all(colour >> 24 == 0xFF for colour in shown)


def test_a_tile_as_argb_has_one_colour_per_pixel_index():
    pixels, shown = tiles.tile_pixels(3), tiles.tile_argb(3)
    assert len(shown) == 256
    assert all(shown[i] == tiles.argb(tiles.ng_colour(pixels[i])) for i in range(256))


def test_write_pair_creates_two_files_of_equal_size(tmp_path):
    names = tiles.write_pair(tmp_path)

    sizes = [(tmp_path / name).stat().st_size for name in names]
    assert sizes == [tiles.TILE_COUNT * 64] * 2
    assert names == tiles.FILE_NAMES


def test_the_rom_folder_links_every_original_file_and_adds_the_pair(tmp_path):
    source = tmp_path / "roms"
    source.mkdir()
    (source / "a.bin").write_bytes(b"one")
    (source / "b.bin").write_bytes(b"two")
    pair_dir = tmp_path / "pair"
    tiles.write_pair(pair_dir)
    target = tmp_path / "rom-c"

    tiles.prepare_rom_dir(source, pair_dir, target)

    assert sorted(p.name for p in target.iterdir()) == sorted(
        ["a.bin", "b.bin", *tiles.FILE_NAMES])
    assert (target / "a.bin").read_bytes() == b"one"
    assert not any(p.name in tiles.FILE_NAMES for p in source.iterdir())


def test_preparing_the_rom_folder_twice_gives_the_same_folder(tmp_path):
    source = tmp_path / "roms"
    source.mkdir()
    (source / "a.bin").write_bytes(b"one")
    pair_dir = tmp_path / "pair"
    tiles.write_pair(pair_dir)
    target = tmp_path / "rom-c"

    tiles.prepare_rom_dir(source, pair_dir, target)
    tiles.prepare_rom_dir(source, pair_dir, target)

    assert sorted(p.name for p in target.iterdir()) == sorted(["a.bin", *tiles.FILE_NAMES])


def test_the_rom_folder_may_not_be_the_folder_it_links_from(tmp_path):
    """It deletes what does not belong in it, so aiming it at the dumps would lose them."""
    source = tmp_path / "roms"
    source.mkdir()
    (source / "a.bin").write_bytes(b"one")
    pair_dir = tmp_path / "pair"
    tiles.write_pair(pair_dir)

    for target in (source, pair_dir):
        with pytest.raises(ValueError, match="folder of its own"):
            tiles.prepare_rom_dir(source, pair_dir, target)

    assert (source / "a.bin").read_bytes() == b"one"
    assert sorted(p.name for p in pair_dir.iterdir()) == sorted(tiles.FILE_NAMES)


def test_preparing_it_again_leaves_the_links_alone(tmp_path):
    source = tmp_path / "roms"
    source.mkdir()
    (source / "a.bin").write_bytes(b"one")
    pair_dir = tmp_path / "pair"
    tiles.write_pair(pair_dir)
    target = tmp_path / "rom-c"
    tiles.prepare_rom_dir(source, pair_dir, target)
    before = (target / "a.bin").stat().st_ino

    tiles.prepare_rom_dir(source, pair_dir, target)

    assert (target / "a.bin").stat().st_ino == before
    assert (target / "a.bin").samefile(source / "a.bin")


def test_a_stale_file_in_the_rom_folder_is_removed(tmp_path):
    source = tmp_path / "roms"
    source.mkdir()
    (source / "a.bin").write_bytes(b"one")
    pair_dir = tmp_path / "pair"
    tiles.write_pair(pair_dir)
    target = tmp_path / "rom-c"
    target.mkdir()
    (target / "old.bin").write_bytes(b"left over")

    tiles.prepare_rom_dir(source, pair_dir, target)

    assert not (target / "old.bin").exists()


def test_the_c_file_writes_the_same_palette_formula():
    """The planter writes the pens itself, so its formula has to be this one.

    Change one side and this test fails: change both, or the capture check of
    `verify_added_space` compares a tile against colours the game never showed.
    """
    source = (Path(tiles.__file__).parent / "added_space_proof.c").read_text()
    for part in ("(pen << 8)", "((15u - pen) << 4)", "((7u * pen) % 16u)"):
        assert part in source, f"added_space_proof.c no longer writes {part}"
