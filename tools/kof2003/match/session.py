"""Owner-recorded sessions and scripted tests that continue them.

log_inputs.lua writes one line per change: "<frames done>\t<button>[+<button>...]"
or "<frames done>\t-". Replayed through replay.lua with REPLAY_OFFSET=1, these
transitions reproduce the recorded session; captures are then labelled one
frame later than the log's frame numbers.
"""


RESET_DAMAGE = ("the input log is damaged: frame numbers must increase and contain no NUL bytes. "
                "A MAME soft reset (F3) while recording causes this; restart MAME instead")


def read_log(text):
    if "\x00" in text:
        raise ValueError(RESET_DAMAGE)
    transitions = []
    for line in text.splitlines():
        frame, held = line.split("\t")
        frame = int(frame)
        if transitions and frame <= transitions[-1][0]:
            raise ValueError(RESET_DAMAGE)
        transitions.append((frame, frozenset() if held == "-" else frozenset(held.split("+"))))
    return transitions


def continue_session(log, cut, script):
    """The session's transitions before `cut`, all buttons released at `cut`, then `script`."""
    if any(event.start < cut for event in script.events):
        raise ValueError(f"the test script starts before the cut at frame {cut}")
    kept = [(frame, held) for frame, held in log if frame < cut]
    following = script.transitions()
    starts_at_cut = bool(following) and following[0][0] == cut
    if kept and kept[-1][1] and not starts_at_cut:
        kept.append((cut, frozenset()))
    return kept + following
