"""Create a private descriptor that loads the original graphics twice."""
import argparse
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PRIVATE = ROOT / 'private'
SIZE = re.compile(rb'(\.crom_size\s*=\s*)0[xX]4000000\b')
PAIRS = re.compile(rb'(\.crom_pairs\s*=\s*\{)(.*?)(\r?\n\s*\},)', re.DOTALL)
PAIR = re.compile(rb'\{\s*"[^"]+"\s*,\s*"[^"]+"\s*\}\s*,')


def prepare(source, destination, expected_hash):
    private = PRIVATE.resolve(strict=True)
    source, destination = source.resolve(strict=True), destination.resolve()
    if not source.is_relative_to(private) or not destination.is_relative_to(private):
        raise ValueError('input and output must be inside private/')
    data = source.read_bytes()
    if hashlib.sha256(data).hexdigest() != expected_hash.lower():
        raise ValueError('descriptor SHA-256 does not match the supplied identity')
    sizes, lists = list(SIZE.finditer(data)), list(PAIRS.finditer(data))
    if len(sizes) != 1 or len(lists) != 1:
        raise ValueError('expected one 64 MiB size and one graphics-pair list')
    pairs = list(PAIR.finditer(lists[0].group(2)))
    if len(pairs) != 4:
        raise ValueError('expected exactly four graphics pairs')
    newline = b'\r\n' if b'\r\n' in data else b'\n'
    extra = b''.join(newline + b'        ' + item.group() for item in pairs)
    cut = lists[0].end(2)
    result = data[:cut] + extra + data[cut:]
    result = SIZE.sub(rb'\g<1>0x8000000', result, count=1)
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
        print(f'Cannot prepare descriptor: {error}', file=sys.stderr)
        return 1
    print(f'Prepared a private 128 MiB descriptor; SHA-256 {digest}.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
