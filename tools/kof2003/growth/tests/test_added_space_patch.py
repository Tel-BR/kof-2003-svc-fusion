"""Turning the private descriptor and renderer into build C, and back again.

The files here are made-up stand-ins, not the third-party ones under private/.
"""
import hashlib

import pytest

from growth import added_space_patch as patch
from growth.added_space_tiles import FILE_NAMES
from growth.graphics_size import MIB_64, MIB_128, read_size

DESCRIPTOR = (
    b"const ng_game_t k_demo = {\n"
    b"    .prom_size = 0x900000,\n"
    b"    .crom_size = 0x4000000,          /* 64 MB after pairing */\n"
    b"    .crom_pairs = {\n"
    b"        {\"a.c1\", \"a.c2\"},\n"
    b"        {\"b.c3\", \"b.c4\"},\n"
    b"        {\"c.c5\", \"c.c6\"},\n"
    b"        {\"d.c7\", \"d.c8\"},\n"
    b"    },\n"
    b"    .srom = \"a.s1\",\n"
    b"};\n"
)

RENDERER = (
    b"static void draw_fix(int scanline, uint32_t *row) {\n"
    b"    (void)scanline; (void)row;\n"
    b"}\n"
    b"\n"
    b"void video_render_line(int line, uint32_t *row) {\n"
    b"    int scanline = line + NG_FIRST_VISIBLE;\n"
    b"    draw_sprites(scanline, row);\n"
    b"}\n"
)


def make(tmp_path, descriptor=DESCRIPTOR, renderer=RENDERER):
    first, second = tmp_path / "game.c", tmp_path / "video.c"
    first.write_bytes(descriptor)
    second.write_bytes(renderer)
    return first, second


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_the_new_pair_is_the_fifth_one(tmp_path):
    descriptor, renderer = make(tmp_path)

    patch.apply(descriptor, renderer)

    text = descriptor.read_text()
    pairs = [line for line in text.splitlines() if line.strip().startswith('{"')]
    assert len(pairs) == 5
    assert all(name in pairs[4] for name in FILE_NAMES)


def test_apply_raises_the_graphics_size_too(tmp_path):
    descriptor, renderer = make(tmp_path)

    patch.apply(descriptor, renderer)

    assert read_size(descriptor) == MIB_128


def test_apply_makes_the_renderer_call_the_planter_under_the_macro(tmp_path):
    descriptor, renderer = make(tmp_path)

    patch.apply(descriptor, renderer)

    body = renderer.read_text()
    assert "#ifdef KOF2003_ADDED_SPACE_PROOF" in body
    assert "kof2003_plant_added_space_sprite();" in body
    # Inside video_render_line, and before anything is drawn on the line.
    assert body.index("kof2003_plant_added_space_sprite();") > body.index("video_render_line")
    assert body.index("kof2003_plant_added_space_sprite();") < body.index("draw_sprites(scanline")


def test_apply_twice_writes_nothing_the_second_time(tmp_path):
    descriptor, renderer = make(tmp_path)
    assert patch.apply(descriptor, renderer) is True
    after_first = digest(descriptor), digest(renderer)

    assert patch.apply(descriptor, renderer) is False

    assert (digest(descriptor), digest(renderer)) == after_first


def test_undo_restores_both_files_byte_for_byte(tmp_path):
    descriptor, renderer = make(tmp_path)
    before = digest(descriptor), digest(renderer)
    patch.apply(descriptor, renderer)

    assert patch.undo(descriptor, renderer) is True

    assert (digest(descriptor), digest(renderer)) == before
    assert read_size(descriptor) == MIB_64


def test_undo_on_untouched_files_changes_nothing(tmp_path):
    descriptor, renderer = make(tmp_path)
    before = digest(descriptor), digest(renderer)

    assert patch.undo(descriptor, renderer) is False

    assert (digest(descriptor), digest(renderer)) == before


def test_windows_line_endings_survive_a_round_trip(tmp_path):
    descriptor, renderer = make(tmp_path, DESCRIPTOR.replace(b"\n", b"\r\n"),
                                RENDERER.replace(b"\n", b"\r\n"))
    before = digest(descriptor), digest(renderer)

    patch.apply(descriptor, renderer)
    for path in (descriptor, renderer):
        assert b"\n" not in path.read_bytes().replace(b"\r\n", b"")
    patch.undo(descriptor, renderer)

    assert (digest(descriptor), digest(renderer)) == before


def test_a_descriptor_that_does_not_hold_four_pairs_is_refused(tmp_path):
    """The Added Space starts at the fifth pair; anywhere else is not tile $80000."""
    for pairs, content in ((9, DESCRIPTOR.replace(b'        {"d.c7", "d.c8"},\n',
                                                  b'        {"d.c7", "d.c8"},\n' * 6)),
                           (3, DESCRIPTOR.replace(b'        {"d.c7", "d.c8"},\n', b""))):
        descriptor, renderer = make(tmp_path, content)
        before = digest(descriptor), digest(renderer)

        with pytest.raises(ValueError, match=f"lists {pairs} pairs"):
            patch.apply(descriptor, renderer)

        assert (digest(descriptor), digest(renderer)) == before


def test_a_renderer_without_the_line_function_is_refused_and_nothing_is_written(tmp_path):
    descriptor, renderer = make(tmp_path, renderer=b"void something_else(void) {}\n")
    before = digest(descriptor), digest(renderer)

    with pytest.raises(ValueError, match="video_render_line"):
        patch.apply(descriptor, renderer)

    assert (digest(descriptor), digest(renderer)) == before, "the descriptor must not change alone"


def test_a_descriptor_without_the_pairs_is_refused(tmp_path):
    descriptor, renderer = make(tmp_path, b"const ng_game_t k_demo = {\n    .crom_size = 0x4000000,\n};\n")

    with pytest.raises(ValueError, match="crom_pairs"):
        patch.apply(descriptor, renderer)


def test_status_reports_both_files(tmp_path):
    descriptor, renderer = make(tmp_path)

    assert patch.state(descriptor, renderer) == patch.State(False, False, MIB_64)
    patch.apply(descriptor, renderer)
    assert patch.state(descriptor, renderer) == patch.State(True, True, MIB_128)


def test_cli_applies_and_undoes_and_prints_hashes(tmp_path, capsys):
    descriptor, renderer = make(tmp_path)
    before = digest(descriptor), digest(renderer)
    where = ["--descriptor", str(descriptor), "--renderer", str(renderer)]

    assert patch.main(["apply", *where]) == 0
    out = capsys.readouterr().out
    assert before[0] in out and digest(descriptor) in out

    assert patch.main(["undo", *where]) == 0
    assert (digest(descriptor), digest(renderer)) == before


def test_the_first_pair_is_where_tile_zero_lives(tmp_path):
    descriptor, _ = make(tmp_path)

    assert patch.first_pair(descriptor) == ("a.c1", "a.c2")


def test_the_first_pair_is_still_the_first_after_a_round_trip(tmp_path):
    descriptor, renderer = make(tmp_path)
    patch.apply(descriptor, renderer)

    assert patch.first_pair(descriptor) == ("a.c1", "a.c2")
