"""Input scripts must mean the same buttons on the native player and on MAME.

Expected values come from the native runtime's own script reader
(neogeorecomp `load_script` / `script_input`), not from this module.
"""
from match.input_script import parse


def test_single_press_is_held_for_six_frames():
    script = parse("1200 coin\n")

    assert script.buttons_at(1199) == frozenset()
    assert script.buttons_at(1200) == {"coin"}
    assert script.buttons_at(1205) == {"coin"}
    assert script.buttons_at(1206) == frozenset()


def test_range_holds_every_frame_from_start_to_end_with_combined_buttons():
    script = parse("16000-16002 b+c\n")

    assert script.buttons_at(15999) == frozenset()
    assert script.buttons_at(16000) == {"b", "c"}
    assert script.buttons_at(16002) == {"b", "c"}
    assert script.buttons_at(16003) == frozenset()


def test_comments_and_blank_lines_are_ignored():
    script = parse("# header\n\n2400 start   # title screen\n")

    assert len(script.events) == 1
    assert script.buttons_at(2400) == {"start"}


def test_unknown_button_is_rejected_with_its_line_number():
    import pytest

    with pytest.raises(ValueError, match="line 2: unknown button 'kick'"):
        parse("1200 coin\n1300 a+kick\n")


def test_transitions_list_each_frame_where_the_held_buttons_change():
    script = parse("1200 coin\n1203-1210 a\n")

    assert script.transitions() == [
        (1200, frozenset({"coin"})),
        (1203, frozenset({"coin", "a"})),
        (1206, frozenset({"a"})),
        (1211, frozenset()),
    ]


def test_lines_the_native_reader_cannot_parse_are_skipped_like_the_player_does():
    script = parse("foo bar\n1200 coin\n1300 a++b+\n")

    assert len(script.events) == 2
    assert script.buttons_at(1300) == {"a", "b"}
