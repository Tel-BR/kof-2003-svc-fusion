"""Write a separate private runtime file whose NEO-PVC byte writes fire the chip's triggers.

KOF 2003 writes the four colour-pack inputs ($2FFFE8-$2FFFEB) one byte at a time and then reads
the packed colour at $2FFFEC. The runtime only ran the colour unpack/pack when the chip was
written as a word, so every packed colour read back as zero and the victory-screen portrait
palette came out all zero (a flat near-black silhouette, ticket 17). The patch makes the byte
handler dispatch the same triggers as the word handler: unpack at word $FF0, pack at $FF4/$FF5,
banking from $FF8. Only the runtime's byte handler changes; the input is never modified.
"""
import argparse
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PRIVATE = ROOT / 'private'
# The unpatched byte handler ends with banking only; the word handler has `word == 0xff0` there.
OLD = (b'    uint32_t word = o >> 1;', b'    if (word >= 0xff8) pvc_bank_update();', b'}')
NEW = (b'    uint32_t word = o >> 1;',
       b'    if (word == 0xff0) pvc_color_unpack();',
       b'    else if (word == 0xff4 || word == 0xff5) pvc_color_pack();',
       b'    if (word >= 0xff8) pvc_bank_update();', b'}')


def prepare(source, destination, expected_hash):
    private = PRIVATE.resolve(strict=True)
    source, destination = source.resolve(strict=True), destination.resolve()
    if not source.is_relative_to(private) or not destination.is_relative_to(private):
        raise ValueError('input and output must be inside private/')
    data = source.read_bytes()
    if hashlib.sha256(data).hexdigest() != expected_hash.lower():
        raise ValueError('runtime SHA-256 does not match the supplied identity')
    newline = b'\r\n' if b'\r\n' in data else b'\n'
    old, new = newline.join(OLD), newline.join(NEW)
    if data.count(old) != 1 or b'static void pvc_w8(' not in data:
        raise ValueError('expected exactly one unpatched PVC byte-write handler')
    # The match must sit inside pvc_w8: no other function header between it and the handler's start.
    start = data.index(b'static void pvc_w8(')
    if data.index(old) < start or b'\nstatic ' in data[start + 1:data.index(old)]:
        raise ValueError('the unpatched tail is not inside the PVC byte-write handler')
    result = data.replace(old, new, 1)
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
        print(f'Cannot prepare PVC byte-write patch: {error}', file=sys.stderr)
        return 1
    print(f'Prepared private runtime file; SHA-256 {digest}.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
