"""Scripted input with the native player's semantics.

The neogeorecomp player reads `<frame>[-<end>] <button>[+<button>...]`.
A single frame is held for six frames so the BIOS can debounce it.
"""
import re
from dataclasses import dataclass

SINGLE_PRESS_FRAMES = 6
# The player's sscanf patterns "%ld-%ld %s", then "%ld %s"; other lines are skipped.
LINE = re.compile(r"\s*(\d+)(?:-(\d+))?\s+(\S+)")
BUTTONS = frozenset({
    "up", "down", "left", "right", "a", "b", "c", "d",
    "p2up", "p2down", "p2left", "p2right", "p2a", "p2b", "p2c", "p2d",
    "start", "start2", "select", "coin", "coin2", "service", "test",
})


@dataclass(frozen=True)
class Event:
    start: int
    end: int
    buttons: frozenset


@dataclass(frozen=True)
class Script:
    events: tuple

    def buttons_at(self, frame):
        held = set()
        for event in self.events:
            if event.start <= frame <= event.end:
                held |= event.buttons
        return frozenset(held)

    def transitions(self):
        """Frames where the held buttons change, with the new held set."""
        edges = sorted({e.start for e in self.events} | {e.end + 1 for e in self.events})
        changes, held = [], frozenset()
        for frame in edges:
            now = self.buttons_at(frame)
            if now != held:
                changes.append((frame, now))
                held = now
        return changes


def parse(text):
    events = []
    for number, line in enumerate(text.splitlines(), start=1):
        match = LINE.match(line.split("#", 1)[0])
        if not match:
            continue
        start = int(match[1])
        end = int(match[2]) if match[2] else start + SINGLE_PRESS_FRAMES - 1
        buttons = match[3]
        names = frozenset(name for name in buttons.split("+") if name)
        for name in sorted(names - BUTTONS):
            raise ValueError(f"line {number}: unknown button '{name}'")
        events.append(Event(start, end, names))
    return Script(tuple(events))
