"""Runs svc_voice_roles.lua against a fake MAME (needs the lupa package; skipped without it)."""
import pytest

from match import svc_voice_roles_report as vr

lupa = pytest.importorskip("lupa.lua54")

FAKE = r"""
local function space()
    local s = {mem = {}, reads = {}, writes = {}}
    function s:read_u8(a) return self.mem[a] or 0 end
    function s:read_u16(a) return self.mem[a] or 0 end
    function s:read_u32(a) return self.mem[a] or 0 end
    function s:install_read_tap(a, b, name, cb) local h = {a = a, b = b, cb = cb} self.reads[#self.reads + 1] = h return h end
    function s:install_write_tap(a, b, name, cb) local h = {a = a, b = b, cb = cb} self.writes[#self.writes + 1] = h return h end
    return s
end
fake = {popups = {}, held = {}, frame_cb = nil}
fake.prog, fake.io = space(), space()
local function cpu(sp) return {spaces = sp, state = {PC = {value = 0}, A4 = {value = 0x10A100}, A7 = {value = 0x10F2D8}}} end
fake.main, fake.audio = cpu({program = fake.prog}), cpu({io = fake.io})
manager = {machine = {
    devices = {[':maincpu'] = fake.main, [':audiocpu'] = fake.audio},
    input = {
        code_from_token = function(self, token) return token end,
        code_pressed = function(self, code) return fake.held[code] == true end},
    popmessage = function(self, text) fake.popups[#fake.popups + 1] = text end}}
emu = {app_version = function() return 'fake' end,
       register_frame_done = function(cb, name) fake.frame_cb = cb end}
function fake.fire(sp, kind, addr, data, mask)
    for _, h in ipairs(sp[kind]) do
        if addr >= h.a and addr <= h.b then h.cb(addr, data, mask) end
    end
end
function fake.frame() fake.frame_cb() end
"""


@pytest.fixture
def session(tmp_path, monkeypatch):
    (tmp_path / "situations.txt").write_text("alpha\tFirst\nbeta\tSecond\n", encoding="utf-8")
    monkeypatch.setenv("VOICE_LOG", str(tmp_path / "log.tsv"))
    monkeypatch.setenv("VOICE_SITUATIONS", str(tmp_path / "situations.txt"))
    runtime = lupa.LuaRuntime()
    runtime.execute(FAKE)
    runtime.execute(vr.LUA.read_text(encoding="utf-8"))
    fake = runtime.globals().fake

    def press(token):
        fake.held[token] = True
        fake.frame()
        fake.held[token] = None
        fake.frame()

    def events():
        return vr.parse_log((tmp_path / "log.tsv").read_text(encoding="utf-8"))

    return runtime, fake, press, events


def table_read(fake, row, word, pc=0x8484, mask=0xFFFF):
    fake.main.state.PC.value = pc
    fake.fire(fake.prog, "reads", 0x0A283C + 2 * row, word, mask)


def test_the_script_loads_and_notes_its_configuration(session, tmp_path):
    first = (tmp_path / "log.tsv").read_text(encoding="utf-8").splitlines()[0]

    assert first.startswith("#voice-roles log") and "block_row=2496" in first and "sits=2" in first


def test_a_table_read_by_the_helper_is_a_request_with_its_slot(session):
    runtime, fake, press, events = session
    fake.prog.mem[0x10A128], fake.prog.mem[0x10A239] = 0x1234, 90

    table_read(fake, 2496 + 7, 0x172D)

    [event] = events()
    assert (event.kind, event.row, event.slot, event.word, event.p1_hp) == ("req", 2503, 7, "172D", 90)
    assert event.p1_anim == "00001234" and event.extra["pc"] == "008484" and event.extra["a4"] == "10A100"


def test_rows_outside_the_block_are_other_and_reads_outside_the_helper_are_reqx(session):
    runtime, fake, press, events = session

    table_read(fake, 206, 0x1A29)
    table_read(fake, 2496 + 79, 0x18B6, pc=0x1000)
    table_read(fake, 2496 + 80, 0x18B6)

    assert [(e.kind, e.slot) for e in events()] == [("req", "other"), ("reqx", 79), ("req", "other")]


def test_the_marker_keys_advance_and_go_back_and_show_the_name(session):
    runtime, fake, press, events = session

    press("KEYCODE_0PAD")
    table_read(fake, 2496, 0x1726)
    press("KEYCODE_0PAD")
    table_read(fake, 2496 + 1, 0x1727)
    press("KEYCODE_DELPAD")
    press("KEYCODE_DELPAD")
    press("KEYCODE_DELPAD")

    got = [(e.kind, e.sit, e.extra.get("id")) for e in events() if e.kind in ("mark", "req")]
    assert got == [("mark", 1, "alpha"), ("req", 1, None), ("mark", 2, "beta"), ("req", 2, None),
                   ("mark", 1, "alpha"), ("mark", 0, "marker0")]
    assert (fake.popups[1], fake.popups[2]) == ("[1/2] First", "[2/2] Second")


def test_holding_a_key_moves_the_marker_once(session):
    runtime, fake, press, events = session

    fake.held["KEYCODE_0PAD"] = True
    for _ in range(5):
        fake.frame()

    assert [e.sit for e in events() if e.kind == "mark"] == [1]


def test_the_marker_stops_at_the_last_situation(session):
    runtime, fake, press, events = session

    for _ in range(4):
        press("KEYCODE_0PAD")

    assert [e.sit for e in events() if e.kind == "mark"] == [1, 2]


def test_stage_latch_and_chip_starts_are_logged(session):
    runtime, fake, press, events = session

    fake.fire(fake.prog, "writes", 0x10C43C, 0x1726, 0xFFFF)
    fake.fire(fake.prog, "writes", 0x320000, 0x2900, 0xFF00)
    fake.fire(fake.prog, "writes", 0x320000, 0x0029, 0x00FF)  # low byte only: ignored
    fake.fire(fake.io, "reads", 0x0000, 0x29, 0xFF)

    def ym(reg, value):
        fake.fire(fake.io, "writes", 0x06, reg, 0xFF)
        fake.fire(fake.io, "writes", 0x07, value, 0xFF)

    for reg, value in ((0x10, 0x29), (0x18, 0x72), (0x20, 0x2F), (0x28, 0x72)):
        ym(reg, value)
    ym(0x00, 0x01)

    got = events()
    assert [(e.kind, e.word) for e in got[:2]] == [("stage", "1726"), ("cmd", "29")]
    assert got[2].kind == "play" and got[2].extra == {"ch": "0", "start": "722900", "end": "722FFF", "latch": "29"}
    assert vr.slots_for_range(0x722900, 0x722FFF) == [0]


def test_a_health_change_is_logged_once(session):
    runtime, fake, press, events = session

    fake.prog.mem[0x10A239] = 80
    fake.frame()
    fake.frame()

    assert [(e.kind, e.extra) for e in events() if e.kind == "hp"] == [("hp", {"p1": "80", "p2": "0"})]
