"""Runs probe.lua's address-list mode against a fake MAME (ticket 08).

Needs the lupa package; skipped without it. Memory values are invented.
"""
from pathlib import Path

import pytest

from match.probe_log import read_log

lupa = pytest.importorskip("lupa.lua54")
PROBE = Path(__file__).resolve().parents[1] / "probe.lua"

FAKE = r"""
fake = {frame_cb = nil, now = 0}
local prog = {}
function prog:read_u8(a) return (a + fake.now) % 0x100 end
function prog:read_u16(a) return (a + fake.now) % 0x10000 end
function prog:read_u32(a) return 0x10000000 + a + fake.now end
manager = {machine = {devices = {[':maincpu'] = {spaces = {program = prog}}}}}
emu = {register_frame_done = function(cb, name) fake.frame_cb = cb end}
function fake.frame() fake.now = fake.now + 1 fake.frame_cb() end
"""


@pytest.fixture
def probe(tmp_path, monkeypatch):
    (tmp_path / "replay.lua").write_text("-- replay stand-in\n")
    monkeypatch.setenv("REPLAY_LUA", str(tmp_path / "replay.lua"))
    monkeypatch.setenv("PROBE_LOG", str(tmp_path / "probe.tsv"))
    for name in ("REPLAY_OFFSET", "PROBE_ADDRESSES", "PROBE_FIRST"):
        monkeypatch.delenv(name, raising=False)

    def start(frames, **env):
        for name, value in env.items():
            monkeypatch.setenv(name, value)
        runtime = lupa.LuaRuntime()
        runtime.execute(FAKE)
        runtime.execute(PROBE.read_text(encoding="utf-8"))
        for _ in range(frames):
            runtime.globals().fake.frame()
        return (tmp_path / "probe.tsv").read_text()
    return start


def test_address_list_is_logged_in_the_native_format_with_replay_frame_labels(probe):
    text = probe(2, PROBE_ADDRESSES="0x1010e0:4,0x2fe91d:1,0x102eac:2")
    assert read_log(text, columns=3) == {
        2: ("101010e1", "1e", "2ead"),
        3: ("101010e2", "1f", "2eae"),
    }


def test_offset_follows_replay_offset(probe):
    text = probe(1, PROBE_ADDRESSES="0x100000:1", REPLAY_OFFSET="1")
    assert text == "1\t01\n"


def test_invalid_address_list_stops_the_script(probe):
    with pytest.raises(lupa.LuaError, match="PROBE_ADDRESSES"):
        probe(0, PROBE_ADDRESSES="0x1010e1:2")
