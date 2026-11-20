"""Add the optional memory probe call to a private copy of the runtime's frame loop (ticket 08).

    python probe_hook.py PRIVATE/neogeo.c PRIVATE/neogeo-probe.c --sha256 HASH

After each frame, the hooked loop calls kof_native_probe(frame) from native_probe.c, but only
when the build defines KOF2003_NATIVE_PROBE (CMake option of the same name). Both paths must
be inside private/; the source must match the given SHA-256; the output must not exist yet.
The hook can sit alongside the rehearsal monitor's hook (import_slot/monitor_hook.py).
"""
import argparse
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PRIVATE = ROOT / 'private'
MARKER = b'        run_frame();'


def prepare(source, destination, expected_hash):
    private = PRIVATE.resolve(strict=True)
    source, destination = Path(source).resolve(strict=True), Path(destination).resolve()
    if not source.is_relative_to(private) or not destination.is_relative_to(private):
        raise ValueError('input and output must be inside private/')
    data = source.read_bytes()
    if hashlib.sha256(data).hexdigest() != expected_hash.lower():
        raise ValueError('runtime SHA-256 does not match the supplied identity')
    if data.count(MARKER) != 1 or b'KOF2003_NATIVE_PROBE' in data:
        raise ValueError('expected one frame hook without the probe')
    newline = b'\r\n' if b'\r\n' in data else b'\n'
    hook = newline.join((MARKER, b'#ifdef KOF2003_NATIVE_PROBE',
                         b'        extern void kof_native_probe(long);',
                         b'        kof_native_probe(frame);', b'#endif'))
    result = data.replace(MARKER, hook, 1)
    with destination.open('xb') as output:
        output.write(result)
    return hashlib.sha256(result).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--sha256', required=True)
    args = parser.parse_args()
    try:
        digest = prepare(args.source, args.destination, args.sha256)
    except (OSError, ValueError) as error:
        print(f'Cannot prepare probe hook: {error}', file=sys.stderr)
        return 1
    print(f'Prepared private runtime probe hook; SHA-256 {digest}.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
