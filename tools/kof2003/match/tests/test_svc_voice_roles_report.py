"""The post-processor of the Guile voice-role session. Synthetic data only: no game data."""
import re
from pathlib import Path

import pytest

from match import svc_voice_roles_report as vr

HEADER = "#frame\tsit\tkind\trow\tslot\tword\tp1_anim\tp1_hp\tp2_anim\tp2_hp\textra\n"
SITUATIONS = vr.read_situations("alpha\tFirst\nbeta\tSecond\ngamma\tThird\n")


def line(frame, sit, kind, row="-", slot="-", word="-", p1_hp=100, extra=""):
    return f"{frame}\t{sit}\t{kind}\t{row}\t{slot}\t{word}\t00000000\t{p1_hp}\t00000000\t100\t{extra}\n"


def req(frame, sit, slot, p1_hp=100):
    row = vr.GUILE_BASE_ROW + slot
    return line(frame, sit, "req", row, slot, f"{vr.SLOTS[slot].word:04X}", p1_hp, "pc=008484 a4=10A100")


def play(frame, sit, start, end, ch=0):
    return line(frame, sit, "play", extra=f"ch={ch} start={start:06X} end={end:06X} latch=09")


def report(*lines):
    return vr.format_report(vr.parse_log(HEADER + "".join(lines)), SITUATIONS)


def test_a_slot_lists_the_situations_where_it_requested_with_counts():
    text = report(line(10, 1, "mark", extra="id=alpha"), req(12, 1, 0), req(40, 1, 0),
                  line(60, 2, "mark", extra="id=beta"), req(62, 2, 0))

    row = next(l for l in text.splitlines() if l.startswith("+0 "))
    assert "req 3" in row and "requested in alpha 2, beta 1" in row


def test_the_same_request_read_twice_in_one_frame_counts_once():
    text = report(line(10, 1, "mark", extra="id=alpha"), req(12, 1, 7), req(12, 1, 7))

    assert "req 1" in next(l for l in text.splitlines() if l.startswith("+7 "))


def test_never_played_lists_every_enabled_slot_without_events():
    assert len(vr.SLOTS) == 38
    text = report(req(12, 1, 0), req(13, 1, 7))

    section = text.split("-- never played: ")[1].splitlines()
    assert section[0].startswith("36 of 38")
    assert "+0" not in section[1].split(", ") and "+7" not in section[1].split(", ")
    assert "+9" in section[1].split(", ") and "+55" in section[1].split(", ")


def test_a_play_counts_by_its_v_range_and_a_shared_range_counts_for_each_slot():
    first = vr.SLOTS[14]
    shared = vr.SLOTS[49]
    text = report(play(20, 1, first.start, first.end), play(30, 1, shared.start, shared.end))

    assert "play 1" in next(l for l in text.splitlines() if l.startswith("+14 "))
    for slot in (49, 50, 55):
        assert "play 1" in next(l for l in text.splitlines() if l.startswith(f"+{slot} "))


def test_a_play_that_starts_inside_a_range_is_matched_when_the_end_differs():
    slot = vr.SLOTS[5]

    assert vr.slots_for_range(slot.start, slot.end - 0x100) == [5]
    assert vr.slots_for_range(0x000000, 0x0000FF) == []


def test_rows_outside_guiles_block_are_summarised_not_counted_as_slots():
    other = line(12, 1, "req", 206, "other", "1A29", extra="pc=008484")
    text = report(other, other.replace("12\t", "14\t", 1))

    assert "row 206 word 1A29: 2x" in text
    assert "never played: 38 of 38" in text


def test_hurt_slots_report_the_health_lost_around_the_request():
    text = report(line(5, 1, "hp", p1_hp=100), req(20, 1, 6, p1_hp=90), line(21, 1, "hp", p1_hp=80))

    row = next(l for l in text.splitlines() if l.startswith("+6 "))
    assert "P1 health lost 20/20/20" in row


def test_a_staged_guile_word_with_no_request_is_flagged_as_a_bypass():
    staged = line(30, 1, "stage", word="172F", extra="addr=10C43C")
    text = report(staged, req(60, 1, 0))

    assert "172F x1" in text.split("-- checks --")[1]


def test_a_staged_word_with_a_request_nearby_is_not_flagged():
    text = report(line(30, 1, "stage", word="1726", extra="addr=10C43C"), req(31, 1, 0))

    assert "staged without a table request within 2 frames: none" in text


def test_situations_are_checked_against_the_research_prediction():
    sits = vr.read_situations(vr.situations_text())

    text = vr.format_report(vr.parse_log(HEADER + "".join([
        line(5, 1, "mark", extra="id=select-guile"), req(6, 1, 0),
        line(50, 5, "mark", extra="id=sanity-light-punch"), req(52, 5, 3)])), sits)

    assert " 1 select-guile: req +0 x1; play -  [unexpected +0]" in text
    assert " 5 sanity-light-punch: req +3 x1; play -  [unexpected +3]  [none seen]" in text


def test_an_empty_log_warns_that_the_hook_may_not_work():
    text = report()

    assert "WARNING: no sound request was logged" in text
    assert "WARNING: no marker was pressed" in text


def test_the_parser_skips_notes_and_broken_lines():
    events = vr.parse_log("#note\n\nnot a line\n" + req(3, 0, 1))

    assert [(e.frame, e.slot, e.word) for e in events] == [(3, 1, "1727")]


def test_the_situations_file_round_trips_and_has_unique_ascii_ids():
    ids = [sid for sid, _, _ in vr.SITUATIONS]

    assert len(ids) == len(set(ids)) == 46
    assert vr.read_situations(vr.situations_text()) == [(sid, label) for sid, label, _ in vr.SITUATIONS]
    assert vr.situations_text().isascii()
    assert all(0 <= s < vr.GUILE_BLOCK_ROWS and s in vr.SLOTS for _, _, exp in vr.SITUATIONS for s in exp)


def test_the_slot_table_matches_the_research_counts():
    assert sorted(vr.SLOTS)[:3] == [0, 1, 2] and len(vr.SLOTS) == 38
    assert all(slot.start % 0x100 == 0 and (slot.end + 1) % 0x100 == 0 for slot in vr.SLOTS.values())
    assert all(vr.GUILE_BASE_ROW + s < vr.GUILE_BASE_ROW + vr.GUILE_BLOCK_ROWS for s in vr.SLOTS)


def test_run_command_uses_the_manual_svc_route_and_the_voice_script(tmp_path):
    out = tmp_path / "run"
    command, environment = vr.build_run(out, Path("mame.exe"), Path("repo"))

    assert command[:3] == ["mame.exe", "svc", "-bios"] and "euro" in command
    assert command[command.index("-autoboot_script") + 1] == str(vr.LUA)
    assert "-ctrlr" in command and "manual-p1" in command
    assert str(Path("repo/private/work/manual-svc/cfg")) in command
    assert environment["VOICE_LOG"] == str(out / "voice_roles.tsv")
    assert environment["VOICE_SITUATIONS"] == str(out / "situations.txt")


def test_the_checklist_lists_exactly_the_situations_in_the_same_order_in_both_languages():
    checklist = (vr.HERE / "svc-voice-roles-checklist.md").read_text(encoding="utf-8")
    english, portuguese = checklist.split("## Português (Brasil)")
    ids = [sid for sid, _, _ in vr.SITUATIONS]

    for half in (english, portuguese):
        found = re.findall(r"^\| (\d+) \| `([a-z0-9-]+)` \|", half, re.M)
        assert [(int(n), sid) for n, sid in found] == list(enumerate(ids, 1))


def test_requests_from_the_p2_object_are_counted_in_the_checks():
    mirror = req(12, 1, 0).replace("a4=10A100", "a4=10A380")

    assert "made from the P2 object (a Guile opponent?): 1" in report(mirror)


def test_the_marker_keys_can_be_overridden_from_the_environment(tmp_path, monkeypatch):
    monkeypatch.setenv("VOICE_KEY_NEXT", "KEYCODE_PGUP")

    _, environment = vr.build_run(tmp_path, Path("mame.exe"), Path("repo"))

    assert environment["VOICE_KEY_NEXT"] == "KEYCODE_PGUP" and environment["VOICE_KEY_BACK"] == vr.KEY_BACK


def test_report_command_reads_a_run_folder(tmp_path, capsys):
    (tmp_path / "situations.txt").write_text(vr.situations_text(), encoding="utf-8")
    (tmp_path / "voice_roles.tsv").write_text(
        HEADER + line(5, 1, "mark", extra="id=select-guile") + req(9, 1, 14), encoding="utf-8")

    vr.main(["report", str(tmp_path)])

    out = capsys.readouterr().out
    assert "+14  0x1734" in out and "requested in select-guile 1" in out
