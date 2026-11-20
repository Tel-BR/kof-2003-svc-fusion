"""Convert a private rehearsal log to a private native-player input script."""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PRIVATE = ROOT / 'private'
EVENT = re.compile(r'\[rehearsal-input\] frame=(\d+) p1=([0-9a-fA-F]{2}) start=([01]) coin=([01])')
FRAME = re.compile(r'\[(?:rehearsal-frame|DEBUG-kyo)\] (\d+) ')
BUTTONS = ((1, 'up'), (2, 'down'), (4, 'left'), (8, 'right'),
           (16, 'a'), (32, 'b'), (64, 'c'), (128, 'd'))


def prepare(source, destination):
    private = PRIVATE.resolve(strict=True)
    source, destination = source.resolve(strict=True), destination.resolve()
    if not source.is_relative_to(private) or not destination.is_relative_to(private):
        raise ValueError('log and output must be inside private/')
    text = source.read_text(encoding='utf-8-sig')
    events = [(int(m[1]), int(m[2], 16), int(m[3]), int(m[4])) for m in EVENT.finditer(text)]
    frames = [int(m[1]) for m in FRAME.finditer(text)]
    if not events or not frames:
        raise ValueError('log must contain input events and per-frame tracing')
    if any(a[0] >= b[0] for a, b in zip(events, events[1:])):
        raise ValueError('input events are not strictly ordered')
    if any(a >= b for a, b in zip(frames, frames[1:])) or events[-1][0] > frames[-1]:
        raise ValueError('frame trace is not strictly ordered or ends before input')
    lines = []
    for index, (start, mask, start_button, coin) in enumerate(events):
        end = events[index + 1][0] - 1 if index + 1 < len(events) else frames[-1]
        names = [name for bit, name in BUTTONS if mask & bit]
        if start_button:
            names.append('start')
        if coin:
            names.append('coin')
        if names:
            lines.append(f'{start}-{end} ' + '+'.join(names))
    with destination.open('x', encoding='utf-8', newline='\n') as output:
        output.write(''.join(line + '\n' for line in lines))
    return len(lines), frames[-1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    try:
        count, frame = prepare(args.source, args.destination)
    except (OSError, UnicodeError, ValueError) as error:
        print(f'Cannot prepare replay: {error}', file=sys.stderr)
        return 1
    print(f'Prepared {count} input intervals through frame {frame} in private/.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
