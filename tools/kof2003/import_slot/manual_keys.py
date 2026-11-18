"""Create a private SDL source with the owner's manual Player 1 keys."""
import argparse
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PRIVATE = ROOT / 'private'
KEYS = dict(UP='SPACE', DOWN='S', LEFT='A', RIGHT='D', Z='KP_4',
            X='KP_5', C='KP_1', V='KP_2')
KEY_PATTERN = re.compile(rb'\bSDL_SCANCODE_(UP|DOWN|LEFT|RIGHT|Z|X|C|V)\b')


def prepare(source, destination, expected_hash):
    private = PRIVATE.resolve(strict=True)
    source, destination = source.resolve(strict=True), destination.resolve()
    if not source.is_relative_to(private) or not destination.is_relative_to(private):
        raise ValueError('input and output must be inside private/')
    data = source.read_bytes()
    if hashlib.sha256(data).hexdigest() != expected_hash.lower():
        raise ValueError('source SHA-256 does not match the supplied identity')
    matches = KEY_PATTERN.findall(data)
    if sorted(matches) != sorted(key.encode() for key in KEYS):
        raise ValueError('expected exactly one of each default Player 1 key')
    result = KEY_PATTERN.sub(lambda match: b'SDL_SCANCODE_' + KEYS[match.group(1).decode()].encode(), data)
    with destination.open('xb') as output:
        output.write(result)
    return hashlib.sha256(result).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--sha256', required=True)
    args = parser.parse_args()
    try:
        digest = prepare(args.source, args.destination, args.sha256)
    except (OSError, ValueError) as error:
        print(f'Cannot prepare manual controls: {error}', file=sys.stderr)
        return 1
    print(f'Prepared private manual controls; SHA-256 {digest}.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
