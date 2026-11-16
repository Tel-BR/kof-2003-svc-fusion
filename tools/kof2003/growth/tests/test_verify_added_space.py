"""Reading a capture and deciding whether the synthetic tile is in it.

The PNGs here are written by the test itself from made-up colours; no game data.
"""
import struct
import zlib

import pytest

from growth import added_space_tiles as tiles
from growth import verify_added_space as verify

PROOF_C = (
    b"#define PROOF_SPRITE   380\n"
    b"#define PROOF_PALETTE  1          /* palette 1, pens 1..15 */\n"
    b"#define PROOF_TILE     0x80000u   /* the first tile of the Added Space */\n"
    b"#define PROOF_X        152\n"
    b"#define PROOF_Y        96\n"
    b"#define PROOF_FIRST_FRAME 1000\n"
)


def write_png(path, width, height, rows, filters=None):
    """An 8-bit RGB PNG. `rows` are lists of (r, g, b); `filters` the per-row filter."""
    raw = b""
    for y, row in enumerate(rows):
        raw += bytes([0 if filters is None else filters[y]])
        raw += b"".join(bytes(pixel) for pixel in row)
    head = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    out = b"\x89PNG\r\n\x1a\n"
    for kind, payload in ((b"IHDR", head), (b"IDAT", zlib.compress(raw)), (b"IEND", b"")):
        out += struct.pack(">I", len(payload)) + kind + payload
        out += struct.pack(">I", zlib.crc32(kind + payload))
    path.write_bytes(out)
    return path


def argb_rows(width, height, colour=(0, 0, 0)):
    return [[colour for _ in range(width)] for _ in range(height)]


def paint_tile(rows, x, y, index):
    """Draw synthetic tile `index` into `rows` the way the renderer would."""
    for row in range(16):
        for column in range(16):
            colour = tiles.tile_argb(index)[row * 16 + column]
            rows[y + row][x + column] = ((colour >> 16) & 0xFF, (colour >> 8) & 0xFF, colour & 0xFF)


def test_constants_come_from_the_c_file(tmp_path):
    source = tmp_path / "proof.c"
    source.write_bytes(PROOF_C)

    assert verify.proof_constants(source) == {"PROOF_TILE": 0x80000, "PROOF_X": 152,
                                              "PROOF_Y": 96, "PROOF_FIRST_FRAME": 1000}


def test_the_real_c_file_still_defines_where_the_sprite_goes():
    constants = verify.proof_constants()

    assert constants["PROOF_TILE"] == tiles.FIRST_TILE
    assert 0 <= constants["PROOF_X"] <= 320 - 16
    assert 0 <= constants["PROOF_Y"] <= 224 - 16
    assert constants["PROOF_FIRST_FRAME"] > 0, "the booting board must be left alone"


def test_every_constant_is_checked_not_just_the_first(tmp_path):
    source = tmp_path / "proof.c"
    source.write_bytes(PROOF_C.replace(b"#define PROOF_Y        96\n", b""))

    with pytest.raises(ValueError, match="PROOF_Y"):
        verify.proof_constants(source)


def test_read_png_gives_back_the_pixels_it_was_written_from(tmp_path):
    rows = [[(1, 2, 3), (4, 5, 6), (7, 8, 9)], [(10, 11, 12), (13, 14, 15), (16, 17, 18)]]
    path = write_png(tmp_path / "a.png", 3, 2, rows)

    image = verify.read_png(path)

    assert (image.width, image.height) == (3, 2)
    assert image.pixels[0] == 0xFF010203
    assert image.pixels[5] == 0xFF101112


def test_read_png_undoes_the_sub_filter(tmp_path):
    # Filter 1 stores each byte as the difference from the byte three places back.
    rows = [[(10, 20, 30), (5, 5, 5)]]
    path = write_png(tmp_path / "b.png", 2, 1, rows, filters=[1])

    image = verify.read_png(path)

    assert image.pixels == [0xFF0A141E, 0xFF0F1923]


def test_read_png_refuses_anything_but_eight_bit_rgb(tmp_path):
    path = tmp_path / "c.png"
    head = struct.pack(">IIBBBBB", 1, 1, 8, 3, 0, 0, 0)  # colour type 3: palette
    body = b"\x89PNG\r\n\x1a\n" + struct.pack(">I", len(head)) + b"IHDR" + head
    path.write_bytes(body + struct.pack(">I", zlib.crc32(b"IHDR" + head)))

    with pytest.raises(ValueError, match="8-bit RGB"):
        verify.read_png(path)


def test_the_tile_is_found_where_the_c_file_puts_it(tmp_path):
    rows = argb_rows(320, 224)
    paint_tile(rows, 152, 96, 0)
    candidate = write_png(tmp_path / "c.png", 320, 224, rows)
    reference = write_png(tmp_path / "b.png", 320, 224, argb_rows(320, 224))

    result = verify.verify(candidate, reference)

    assert result.at == (152, 96)
    assert result.matched and result.wrong_pixels == 0
    assert result.reference_matched is False


def test_one_wrong_pixel_is_counted_and_fails(tmp_path):
    rows = argb_rows(320, 224)
    paint_tile(rows, 152, 96, 0)
    rows[96][152] = (0, 0, 0)
    candidate = write_png(tmp_path / "c.png", 320, 224, rows)

    result = verify.verify(candidate)

    assert not result.matched
    assert result.wrong_pixels == 1
    assert result.reference_matched is None


def test_the_tile_in_the_reference_too_is_reported(tmp_path):
    rows = argb_rows(320, 224)
    paint_tile(rows, 152, 96, 0)
    both = write_png(tmp_path / "c.png", 320, 224, rows)

    result = verify.verify(both, both)

    assert result.matched
    assert result.reference_matched is True


def test_a_capture_of_the_wrong_size_is_refused(tmp_path):
    small = write_png(tmp_path / "c.png", 32, 32, argb_rows(32, 32))

    with pytest.raises(ValueError, match="320x224"):
        verify.verify(small)


def test_cli_passes_only_when_the_tile_is_in_the_candidate_alone(tmp_path, capsys):
    rows = argb_rows(320, 224)
    paint_tile(rows, 152, 96, 0)
    candidate = write_png(tmp_path / "c.png", 320, 224, rows)
    reference = write_png(tmp_path / "b.png", 320, 224, argb_rows(320, 224))

    assert verify.main([str(candidate), str(reference)]) == 0
    assert "the synthetic tile is there" in capsys.readouterr().out
    assert verify.main([str(candidate), str(candidate)]) == 1
