"""Voice-role session for Guile in SVC Chaos (wayfinder ticket 33): launch MAME, then read the log.

    py -3 -m match.svc_voice_roles_report run            # situations file + MAME + report, one go
    py -3 -m match.svc_voice_roles_report report RUN_DIR  # report again (or: report FILE.tsv)
    py -3 -m match.svc_voice_roles_report situations FILE # only write the situations list

`run` makes private/work/mame-runs/voice-roles-<time>/ with situations.txt, voice_roles.tsv (written
by svc_voice_roles.lua), mame.log and report.txt. The report lists, for each of Guile's enabled
sound slots (rows 2496 to 2575, slots +0 to +79), the situations in which it played, and the slots
that never played. It carries only frame numbers, row numbers, sample address ranges and situation
names; the TSV is a game trace and stays under private/.
"""
import argparse
import os
import statistics
import subprocess
import sys
from collections import Counter, defaultdict, namedtuple
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MAME = Path(os.environ.get("KOF2003_MAME", Path.home() / "MAME" / "mame.exe"))
LUA = HERE / "svc_voice_roles.lua"
TSV_NAME = "voice_roles.tsv"
SITUATIONS_NAME = "situations.txt"
KEY_NEXT = "KEYCODE_0PAD"
KEY_BACK = "KEYCODE_DELPAD"

GUILE_BASE_ROW = 2496
GUILE_BLOCK_ROWS = 80
P1_OBJECT = 0x10A100  # default of probe.lua; override with PROBE_P1_OBJECT in the Lua script only

Slot = namedtuple("Slot", "word start end role")

# The 38 enabled rows of Guile's block, from research 30 (words, V ranges, inferred roles).
SLOTS = {
    0: Slot(0x1726, 0x722900, 0x722FFF, "attack voice, low tier (known)"),
    1: Slot(0x1727, 0x724A00, 0x7251FF, "attack voice, Guard Cancel Attack (known)"),
    2: Slot(0x1728, 0x635B00, 0x636BFF, "third attack tier (inferred)"),
    3: Slot(0x1729, 0x633700, 0x6347FF, "no static trigger"),
    4: Slot(0x172A, 0x71F300, 0x71FCFF, "no static trigger"),
    5: Slot(0x172B, 0x725200, 0x725BFF, "throw (inferred)"),
    6: Slot(0x172C, 0x723700, 0x7241FF, "hurt, medium (inferred)"),
    7: Slot(0x172D, 0x723000, 0x7236FF, "hurt, light (inferred)"),
    8: Slot(0x172E, 0x5AD900, 0x5AF1FF, "hurt, heavy or launch (inferred)"),
    9: Slot(0x172F, 0x334400, 0x337AFF, "knockout (inferred)"),
    10: Slot(0x1730, 0x52C900, 0x52E5FF, "no static trigger"),
    11: Slot(0x1731, 0x3A6700, 0x3A94FF, "no static trigger"),
    12: Slot(0x1732, 0x5A3B00, 0x5A55FF, "no static trigger"),
    14: Slot(0x1734, 0x52AD00, 0x52C8FF, "taunt (inferred)"),
    15: Slot(0x1735, 0x4AE000, 0x4B00FF, "move record 0x04FA12 voice"),
    16: Slot(0x1736, 0x5A5600, 0x5A6FFF, "move record 0x04FD88 voice"),
    17: Slot(0x1737, 0x71FD00, 0x7208FF, "move record 0x0500E0 voice"),
    18: Slot(0x1738, 0x720900, 0x7213FF, "move record 0x0500E0 voice"),
    19: Slot(0x1739, 0x6A6200, 0x6A6FFF, "move record 0x0500E0 voice"),
    20: Slot(0x173A, 0x5A7000, 0x5A8AFF, "move record 0x0500E0 function voice"),
    21: Slot(0x173B, 0x5A8B00, 0x5AA4FF, "action 0x33 function voice"),
    22: Slot(0x173C, 0x721400, 0x721EFF, "move record 0x0503D6 voice"),
    23: Slot(0x173D, 0x721F00, 0x7228FF, "move record 0x0503D6 voice"),
    24: Slot(0x173E, 0x634800, 0x635AFF, "move record 0x0503D6 voice"),
    25: Slot(0x173F, 0x5AA500, 0x5ABDFF, "move record 0x04FB1C voice (class unresolved)"),
    26: Slot(0x1740, 0x5ABE00, 0x5AD8FF, "move record 0x04FB1C voice (class unresolved)"),
    27: Slot(0x1741, 0x3A9500, 0x3AC2FF, "move record 0x04FF26 voice"),
    28: Slot(0x1733, 0x725C00, 0x7263FF, "no static trigger"),
    29: Slot(0x1BBC, 0x726400, 0x726DFF, "no static trigger"),
    30: Slot(0x1BBD, 0x724200, 0x7249FF, "no static trigger"),
    31: Slot(0x1BBE, 0x41C900, 0x41F0FF, "hurt, launch (inferred)"),
    48: Slot(0x1F50, 0x37C800, 0x37FFFF, "Guile-only effect, record 0x04FA12"),
    49: Slot(0x16A5, 0x7DC800, 0x7DECFF, "shared effect"),
    50: Slot(0x16A5, 0x7DC800, 0x7DECFF, "shared effect"),
    51: Slot(0x1F51, 0x1FBE00, 0x1FFFFF, "Guile-only effect, record 0x04FB1C"),
    53: Slot(0x16AF, 0x556800, 0x5585FF, "shared effect"),
    54: Slot(0x1F1B, 0x83CD00, 0x83E3FF, "shared effect"),
    55: Slot(0x16A5, 0x7DC800, 0x7DECFF, "shared effect"),
}

HURT_ANY = (6, 7, 8, 31)
SPECIAL_VOICES = (15, 16, 25, 26, 48, 49, 51)
SUPER_VOICES = (17, 18, 19, 20, 21, 22, 23, 24, 27, 50, 54)
ATTACKS = (0, 2)

# id, short label for the on-screen marker (ASCII only), slots research 30 predicts (others get a *).
SITUATIONS = [
    ("select-guile", "Selecao: cursor no Guile e confirmar", ()),
    ("pre-fight-dialogue", "Dialogo antes da luta", ()),
    ("round-start", "Inicio do round ate aparecer FIGHT", ()),
    ("movement-only", "So andar, pular e abaixar, sem golpes", ()),
    ("sanity-light-punch", "Soco leve A em pe, 10 vezes", (0,)),
    ("sanity-light-kick", "Chute leve B em pe, 10 vezes", (0,)),
    ("strong-standing", "Golpes fortes C e D em pe, 10 de cada", ATTACKS),
    ("crouch-normals", "Agachado: A, B, C e D, 5 de cada", ATTACKS),
    ("jump-normals", "No pulo: A, B, C e D, 5 de cada", ATTACKS),
    ("knee-bazooka", "Knee Bazooka: frente ou tras + B", ATTACKS + SPECIAL_VOICES),
    ("rolling-sobat", "Rolling Sobat: frente ou tras + D", ATTACKS + SPECIAL_VOICES),
    ("slide-kick", "Slide Kick: baixo-frente + B", ATTACKS + SPECIAL_VOICES),
    ("spin-back-knuckle", "Spin Back Knuckle: frente + C", ATTACKS + SPECIAL_VOICES),
    ("sonic-boom-a", "Sonic Boom com A", SPECIAL_VOICES),
    ("sonic-boom-c", "Sonic Boom com C", SPECIAL_VOICES),
    ("somersault-kick-b", "Somersault Kick com B", SPECIAL_VOICES),
    ("somersault-kick-d", "Somersault Kick com D", SPECIAL_VOICES),
    ("throw-ground", "Guile arremessa o CPU, no chao", (5,)),
    ("throw-air", "Arremesso no ar (se existir)", (5,)),
    ("taunt", "Provocacao (Start), 5 vezes", (14,)),
    ("super-somersault-slash", "Super 1: Somersault Slash (soco)", SUPER_VOICES),
    ("super-somersault-strike", "Super 2: Somersault Strike (chute)", SUPER_VOICES),
    ("super-total-wipeout", "Super 3: Total Wipeout (chute)", SUPER_VOICES),
    ("guard-cancel-attack", "Defendendo, C+D (Guard Cancel Attack)", (1,)),
    ("hurt-light", "Guile apanha de golpe LEVE, 10 acertos", (7,)),
    ("hurt-medium", "Guile apanha de golpe MEDIO, 10 acertos", (6,)),
    ("hurt-heavy", "Guile apanha de golpe FORTE, 10 acertos", (8,)),
    ("hurt-launch", "Guile lancado ao ar ou jogado longe", (31, 8)),
    ("hurt-knockdown", "Guile derrubado no chao, sem KO", (8, 9, 31)),
    ("hurt-crouch", "Guile acertado agachado", HURT_ANY),
    ("hurt-air", "Guile acertado no pulo", HURT_ANY),
    ("hurt-projectile", "Guile acertado por projetil", HURT_ANY),
    ("hurt-super", "Guile acertado por super do CPU", HURT_ANY + (9,)),
    ("thrown", "CPU arremessa o Guile", HURT_ANY),
    ("guard-crush", "Defender ate a guarda quebrar", ()),
    ("exceed", "Exceed (vida na metade): 2 socos", SPECIAL_VOICES + SUPER_VOICES),
    ("max-mode", "Barra cheia: modo MAX", ()),
    ("ko-guile", "Guile nocauteado, ultimo golpe do round", (9,)),
    ("lose-pose", "Round perdido: Guile no chao", ()),
    ("round-start-2", "Inicio do round seguinte", ()),
    ("ko-opponent", "Guile nocauteia o CPU, ultimo golpe", ()),
    ("ko-opponent-special", "Nocautear o CPU com especial ou super", SPECIAL_VOICES + SUPER_VOICES),
    ("win-round", "Pose de vitoria do round", ()),
    ("win-match", "Vitoria da luta: pose e fala final", ()),
    ("time-over", "Tempo esgotado (opcional)", ()),
    ("continue-screen", "Tela de continue ou game over", ()),
]

Event = namedtuple("Event", "frame sit kind row slot word p1_anim p1_hp p2_anim p2_hp extra")


def situations_text():
    """The text of the situations file: '<id><TAB><label>' per line, in marker order."""
    return "".join(f"{sid}\t{label}\n" for sid, label, _ in SITUATIONS)


def read_situations(text):
    """[(id, label)] from a situations file; marker N is entry N (marker 0 is before the first)."""
    rows = []
    for line in text.splitlines():
        line = line.rstrip("\r")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        sid, _, label = line.partition("\t")
        rows.append((sid, label or sid))
    return rows


def parse_extra(text):
    pairs = (part.partition("=") for part in text.split())
    return {key: value for key, sep, value in pairs if sep}


def parse_log(text):
    """Events of a voice_roles.tsv; '#' lines and lines that are not events are skipped."""
    events = []
    for line in text.splitlines():
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) < 10 or not parts[0].isdigit():
            continue
        extra = parse_extra(parts[10]) if len(parts) > 10 else {}
        slot = parts[4]
        slot = int(slot) if slot.lstrip("-").isdigit() else (slot if slot != "-" else None)
        row = int(parts[3]) if parts[3].isdigit() else None
        events.append(Event(int(parts[0]), int(parts[1]), parts[2], row, slot, parts[5],
                            parts[6], int(parts[7]), parts[8], int(parts[9]), extra))
    return events


def situation_name(situations, index):
    if index == 0:
        return "(before the first marker)"
    if 0 < index <= len(situations):
        return situations[index - 1][0]
    return f"marker{index}"


def slots_for_range(start, end):
    """Slots whose V range is exactly start..end, else those whose range contains start."""
    exact = [s for s, slot in SLOTS.items() if (slot.start, slot.end) == (start, end)]
    if exact:
        return exact
    return [s for s, slot in SLOTS.items() if slot.start <= start <= slot.end]


def slots_for_word(word):
    return [s for s, slot in SLOTS.items() if slot.word == word]


def damage(series, frame):
    """P1 health lost around a request: last value up to frame-2 minus the lowest in frame-1..frame+6."""
    before = None
    after = []
    for f, hp in series:
        if f <= frame - 2:
            before = hp
        elif frame - 1 <= f <= frame + 6:
            after.append(hp)
    if before is None or not after:
        return None
    return max(0, before - min(after))


def analyze(events, situations):
    series = sorted({(e.frame, e.p1_hp) for e in events})
    per_slot = defaultdict(lambda: {"req": set(), "play": set(), "dmg": []})
    by_situation = defaultdict(lambda: {"req": Counter(), "play": Counter()})
    other = defaultdict(lambda: {"count": 0, "sits": Counter()})
    reqx = Counter()
    for e in events:
        if e.kind == "req":
            key = (e.frame, e.row, e.word)
            if isinstance(e.slot, int) and e.slot in SLOTS:
                entry = per_slot[e.slot]
                if key not in entry["req"]:
                    entry["req"].add(key)
                    entry.setdefault("sits", Counter())[e.sit] += 1
                    by_situation[e.sit]["req"][e.slot] += 1
                    lost = damage(series, e.frame)
                    if lost is not None and e.slot in (6, 7, 8, 9, 31):
                        entry["dmg"].append(lost)
            elif e.slot == "other" or isinstance(e.slot, int):
                other[(e.row, e.word)]["count"] += 1
                other[(e.row, e.word)]["sits"][e.sit] += 1
        elif e.kind == "reqx":
            reqx[e.slot if isinstance(e.slot, int) else "other"] += 1
        elif e.kind == "play":
            start = int(e.extra.get("start", "0"), 16)
            end = int(e.extra.get("end", "0"), 16)
            key = (e.frame, e.extra.get("ch"), start, end)
            for slot in slots_for_range(start, end):
                entry = per_slot[slot]
                if key not in entry["play"]:
                    entry["play"].add(key)
                    entry.setdefault("play_sits", Counter())[e.sit] += 1
                    by_situation[e.sit]["play"][slot] += 1
    return per_slot, by_situation, other, reqx


def _sits(counter, situations, limit=6):
    parts = [f"{situation_name(situations, s)} {n}" for s, n in sorted(counter.items())]
    return ", ".join(parts[:limit]) + (f", +{len(parts) - limit} more" if len(parts) > limit else "")


def _slot_list(counter):
    return ", ".join(f"+{s} x{n}" for s, n in sorted(counter.items())) or "-"


def bypass_check(events):
    """Guile words staged with no table request within two frames: a request the hook missed."""
    requests = defaultdict(list)
    for e in events:
        if e.kind == "req":
            requests[e.word].append(e.frame)
    missed = Counter()
    for e in events:
        if e.kind != "stage" or e.word == "----" or not slots_for_word(int(e.word, 16)):
            continue
        if not any(abs(f - e.frame) <= 2 for f in requests.get(e.word, [])):
            missed[e.word] += 1
    return missed


def format_report(events, situations):
    per_slot, by_situation, other, reqx = analyze(events, situations)
    marks = [e for e in events if e.kind == "mark"]
    kinds = Counter(e.kind for e in events)
    frames = [e.frame for e in events]
    lines = ["== Guile voice roles, SVC Chaos (ticket 33) =="]
    lines.append(f"events: {len(events)} ({', '.join(f'{k} {n}' for k, n in sorted(kinds.items()))}); "
                 f"frames {min(frames) if frames else 0}-{max(frames) if frames else 0}")
    reached = {e.sit for e in events if e.sit > 0}
    lines.append(f"markers pressed: {len(marks)}; situations reached: {len(reached)} of {len(situations)}")
    if not kinds.get("req"):
        lines.append("WARNING: no sound request was logged. The hook may not work (see the checklist).")
    if not marks:
        lines.append("WARNING: no marker was pressed, so every event belongs to situation 0.")

    lines += ["", "-- per slot: Guile block, enabled rows (req = table requests, play = chip started the V range) --"]
    for slot, info in SLOTS.items():
        entry = per_slot.get(slot)
        reqs = len(entry["req"]) if entry else 0
        plays = len(entry["play"]) if entry else 0
        head = f"+{slot:<3} 0x{info.word:04X} 0x{info.start:06X}-0x{info.end:06X} {info.role}"
        if not reqs and not plays:
            lines.append(f"{head}: never")
            continue
        text = f"{head}: req {reqs}, play {plays}"
        if entry and entry.get("sits"):
            text += f"; requested in {_sits(entry['sits'], situations)}"
        if entry and entry.get("play_sits"):
            text += f"; played in {_sits(entry['play_sits'], situations)}"
        if entry and entry["dmg"]:
            d = entry["dmg"]
            text += f"; P1 health lost {min(d)}/{statistics.median(d):g}/{max(d)} (min/median/max, n={len(d)})"
        lines.append(text)

    never = [s for s in SLOTS if not per_slot.get(s) or not (per_slot[s]["req"] or per_slot[s]["play"])]
    lines += ["", f"-- never played: {len(never)} of {len(SLOTS)} enabled slots --"]
    lines.append(", ".join(f"+{s}" for s in never) or "none")

    lines += ["", "-- per situation (Guile slots; unexpected = not predicted by research 30, none seen = predicted slots missing) --"]
    expected = {sid: set(exp) for sid, _, exp in SITUATIONS}
    for index in range(1, len(situations) + 1):
        sid = situations[index - 1][0]
        seen = by_situation[index]["req"] if index in by_situation else Counter()
        plays = by_situation[index]["play"] if index in by_situation else Counter()
        if index not in reached:
            continue
        flag = ""
        if sid in expected:
            extra_slots = sorted(s for s in set(seen) | set(plays) if s not in expected[sid])
            if extra_slots:
                flag += "  [unexpected " + ", ".join(f"+{s}" for s in extra_slots) + "]"
            if expected[sid] and not (set(seen) | set(plays)) & expected[sid]:
                flag += "  [none seen]"
        lines.append(f"{index:>2} {sid}: req {_slot_list(seen)}; play {_slot_list(plays)}{flag}")
    skipped = [situations[i - 1][0] for i in range(1, len(situations) + 1) if i not in reached]
    if skipped:
        lines.append("not reached: " + ", ".join(skipped))
    if 0 in by_situation and by_situation[0]["req"]:
        lines.append("before the first marker (situation 0): req " + _slot_list(by_situation[0]["req"]))

    lines += ["", "-- other rows (outside Guile's block: the opponent, the system, shared effects), top 15 --"]
    for (row, word), info in sorted(other.items(), key=lambda kv: -kv[1]["count"])[:15]:
        lines.append(f"row {row} word {word}: {info['count']}x in {_sits(info['sits'], situations, 3)}")
    if not other:
        lines.append("none")

    missed = bypass_check(events)
    lines += ["", "-- checks --"]
    lines.append("table reads outside the helper window (reqx): "
                 + (", ".join(f"{k} x{v}" for k, v in sorted(reqx.items(), key=str)) or "none"))
    lines.append("Guile words staged without a table request within 2 frames: "
                 + (", ".join(f"{w} x{n}" for w, n in sorted(missed.items())) or "none"))
    from_p2 = sum(1 for e in events if e.kind == "req" and isinstance(e.slot, int)
                  and e.extra.get("a4", "").upper().endswith("10A380"))
    lines.append(f"Guile-block requests made from the P2 object (a Guile opponent?): {from_p2}")
    return "\n".join(lines) + "\n"


def build_run(out_dir, mame=MAME, root=ROOT):
    """MAME command and environment for the manual SVC session (same route as Start-ManualMvs.ps1)."""
    profile = root / "private" / "work" / "manual-svc"
    command = [str(mame), "svc", "-bios", "euro", "-noreadconfig", "-skip_gameinfo",
               "-rompath", f"{root / 'private' / 'dumps' / 'svc'};{root / 'private' / 'bios'}",
               "-ctrlrpath", str(HERE.parent), "-ctrlr", "manual-p1",
               "-cfg_directory", str(profile / "cfg"), "-nvram_directory", str(profile / "nvram"),
               "-snapshot_directory", str(out_dir),
               "-window", "-maximize", "-video", "gdi", "-autoboot_script", str(LUA)]
    environment = dict(os.environ, VOICE_LOG=str(out_dir / TSV_NAME),
                       VOICE_SITUATIONS=str(out_dir / SITUATIONS_NAME),
                       VOICE_KEY_NEXT=os.environ.get("VOICE_KEY_NEXT", KEY_NEXT),
                       VOICE_KEY_BACK=os.environ.get("VOICE_KEY_BACK", KEY_BACK))
    return command, environment


def report_for(path):
    path = Path(path)
    tsv = path / TSV_NAME if path.is_dir() else path
    situations_file = tsv.parent / SITUATIONS_NAME
    situations = read_situations(situations_file.read_text(encoding="utf-8")) \
        if situations_file.exists() else read_situations(situations_text())
    return format_report(parse_log(tsv.read_text(encoding="utf-8", errors="replace")), situations)


def run(mame):
    if not Path(mame).exists():
        sys.exit(f"MAME not found at {mame}. Set KOF2003_MAME to the full path of mame.exe.")
    out = ROOT / "private" / "work" / "mame-runs" / f"voice-roles-{datetime.now():%Y%m%d-%H%M%S}"
    out.mkdir(parents=True)
    (out / SITUATIONS_NAME).write_text(situations_text(), encoding="utf-8")
    command, environment = build_run(out, mame)
    for name in ("cfg", "nvram"):
        (ROOT / "private" / "work" / "manual-svc" / name).mkdir(parents=True, exist_ok=True)
    print(f"Run folder: {out}\nMAME opens now. Keys: keypad 0 = next situation, keypad . = back. "
          "Close MAME when done.", flush=True)
    with (out / "mame.log").open("w") as log:
        subprocess.run(command, cwd=Path(mame).parent, env=environment, stdout=log,
                       stderr=subprocess.STDOUT, check=False)
    if not (out / TSV_NAME).exists():
        sys.exit(f"No log was written. Look at {out / 'mame.log'}.")
    text = report_for(out)
    (out / "report.txt").write_text(text, encoding="utf-8")
    print(text)
    print(f"Send back: {out / TSV_NAME} and {out / 'report.txt'}")


def main(argv=None):
    options = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = options.add_subparsers(dest="command", required=True)
    runner = sub.add_parser("run", help="write the situations file, start MAME, print the report")
    runner.add_argument("--mame", type=Path, default=MAME)
    reporter = sub.add_parser("report", help="print the report of a run folder or a .tsv")
    reporter.add_argument("path", type=Path)
    writer = sub.add_parser("situations", help="write the situations file")
    writer.add_argument("path", type=Path)
    args = options.parse_args(argv)
    if args.command == "run":
        run(args.mame)
    elif args.command == "report":
        print(report_for(args.path))
    else:
        args.path.write_text(situations_text(), encoding="utf-8")
        print(args.path)


if __name__ == "__main__":
    main()
