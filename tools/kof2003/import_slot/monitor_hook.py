"""Write a separate private runtime file with an optional rehearsal log hook."""
import argparse
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PRIVATE = ROOT / 'private'
MARKER = b'    run_frame();'


def prepare(source, destination, expected_hash):
    private = PRIVATE.resolve(strict=True)
    source, destination = source.resolve(strict=True), destination.resolve()
    if not source.is_relative_to(private) or not destination.is_relative_to(private):
        raise ValueError('input and output must be inside private/')
    data = source.read_bytes()
    if hashlib.sha256(data).hexdigest() != expected_hash.lower():
        raise ValueError('runtime SHA-256 does not match the supplied identity')
    if data.count(MARKER) != 1 or b'KOF2003_REHEARSAL_MONITOR' in data:
        raise ValueError('expected one unmodified frame hook')
    newline = b'\r\n' if b'\r\n' in data else b'\n'
    hook = newline.join((MARKER, b'#ifdef KOF2003_REHEARSAL_MONITOR',
                         b'        extern void kof_rehearsal_monitor(long, const ng_input_t *);',
                         b'        kof_rehearsal_monitor(frame, &in);', b'#endif'))
    result = data.replace(MARKER, hook, 1)
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
        print(f'Cannot prepare monitor hook: {error}', file=sys.stderr)
        return 1
    print(f'Prepared private runtime hook; SHA-256 {digest}.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
