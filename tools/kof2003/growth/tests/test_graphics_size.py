"""Raising and lowering the graphics size in the cartridge descriptor.

The files here are made-up descriptors, not the third-party one under private/.
Expected values are written out by hand.
"""
import hashlib

import pytest

from growth.graphics_size import MIB_128, MIB_64, apply, main, read_size, undo

DESCRIPTOR = (
    b"const ng_game_t k_demo = {\n"
    b"    .prom_size = 0x900000,           /* 1 MB fixed + 8 MB banked */\n"
    b"    .crom_size = 0x4000000,          /* 64 MB after pairing */\n"
    b"    .crom_pairs = {\n"
    b"        {\"a.c1\", \"a.c2\"},\n"
    b"    },\n"
    b"};\n"
)


def make(tmp_path, content=DESCRIPTOR):
    path = tmp_path / "game.c"
    path.write_bytes(content)
    return path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_reads_the_size_from_the_descriptor(tmp_path):
    assert read_size(make(tmp_path)) == MIB_64


def test_apply_raises_only_the_size_value(tmp_path):
    path = make(tmp_path)

    assert apply(path) is True

    expected = DESCRIPTOR.replace(b".crom_size = 0x4000000,", b".crom_size = 0x8000000,")
    assert path.read_bytes() == expected
    assert read_size(path) == MIB_128


def test_apply_twice_changes_nothing_the_second_time(tmp_path):
    path = make(tmp_path)
    apply(path)
    after_first = digest(path)

    assert apply(path) is False

    assert digest(path) == after_first


def test_undo_restores_the_original_bytes(tmp_path):
    path = make(tmp_path)
    before = digest(path)
    apply(path)

    assert undo(path) is True

    assert digest(path) == before


def test_undo_on_the_original_changes_nothing(tmp_path):
    path = make(tmp_path)
    before = digest(path)

    assert undo(path) is False

    assert digest(path) == before


def test_windows_line_endings_survive_a_round_trip(tmp_path):
    path = make(tmp_path, DESCRIPTOR.replace(b"\n", b"\r\n"))
    before = digest(path)

    apply(path)
    assert b"\r\n" in path.read_bytes() and b"\n" not in path.read_bytes().replace(b"\r\n", b"")
    undo(path)

    assert digest(path) == before


def test_a_descriptor_without_the_size_is_refused(tmp_path):
    path = make(tmp_path, b"const ng_game_t k_demo = {};\n")
    with pytest.raises(ValueError, match="crom_size"):
        read_size(path)


def test_two_size_lines_are_refused(tmp_path):
    path = make(tmp_path, DESCRIPTOR + DESCRIPTOR)
    with pytest.raises(ValueError, match="more than once"):
        apply(path)


def test_an_unknown_size_is_refused_and_left_alone(tmp_path):
    path = make(tmp_path, DESCRIPTOR.replace(b"0x4000000", b"0x2000000"))
    before = digest(path)
    with pytest.raises(ValueError, match="0x2000000"):
        apply(path)
    assert digest(path) == before


def test_cli_prints_hashes_before_and_after(tmp_path, capsys):
    path = make(tmp_path)
    before = digest(path)

    assert main(["apply", "--descriptor", str(path)]) == 0

    out = capsys.readouterr().out
    assert before in out and digest(path) in out
    assert "0x8000000" in out


def test_cli_status_changes_nothing(tmp_path, capsys):
    path = make(tmp_path)
    before = digest(path)

    assert main(["status", "--descriptor", str(path)]) == 0

    assert digest(path) == before
    assert "64 MiB" in capsys.readouterr().out


def test_cli_missing_descriptor_is_an_error(tmp_path):
    with pytest.raises(SystemExit):
        main(["status", "--descriptor", str(tmp_path / "nope.c")])
