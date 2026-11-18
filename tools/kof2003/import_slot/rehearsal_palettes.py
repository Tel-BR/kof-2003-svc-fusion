"""Give the private rehearsal clone four independently varied palettes."""
import argparse
import colorsys
import hashlib
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PRIVATE = ROOT / 'private'
PROGRAM_SIZE = 0x900000
TABLES = (0x6090A, 0x6098A, 0x60A0A, 0x60A8A)
PALETTE_BANK = 0x100000
DESTINATION_INDEX = 0x2D00
SLOTS = 16
PALETTE_SIZE = 32
IMPORTED_ID = 0x30


def adjust(word, direction):
    fields = ((8, 14), (4, 13), (0, 12))
    original = [(((word >> high) & 15) << 1) | ((word >> low) & 1)
                for high, low in fields]
    rgb = [value / 31 for value in original]
    hue, saturation, value = colorsys.rgb_to_hsv(*rgb)
    if saturation == 0:
        # A neutral has no hue to rotate; give it a small red/blue tint.
        hue = 0 if direction > 0 else 2 / 3
        value = max(value, 3 / 31)
        saturation = min(1, 3 / (value * 31))
        shifted = hue
    else:
        shifted = ((hue * 360 + 30 * direction) % 360) / 360
    proposed = colorsys.hsv_to_rgb(shifted, saturation, value)
    channels = [max(0, min(31, max(old - 3, min(old + 3, math.floor(new * 31 + 0.5)))))
                for old, new in zip(original, proposed)]
    result = word & 0x8000
    for channel, (high_bit, low_bit) in zip(channels, fields):
        result |= (channel >> 1) << high_bit
        result |= (channel & 1) << low_bit
    return result


def prepare(source, destination, expected_hash, fighter_id):
    private = PRIVATE.resolve(strict=True)
    source, destination = source.resolve(strict=True), destination.resolve()
    if not source.is_relative_to(private) or not destination.is_relative_to(private):
        raise ValueError('input and output must be inside private/')
    if not 0 <= fighter_id < 37:
        raise ValueError('fighter ID must be original')
    data = source.read_bytes()
    if len(data) != PROGRAM_SIZE or hashlib.sha256(data).hexdigest() != expected_hash.lower():
        raise ValueError('program size or SHA-256 does not match the supplied identity')
    indices = [int.from_bytes(data[base + fighter_id * 2:base + fighter_id * 2 + 2], 'big')
               for base in TABLES]
    for base, index in zip(TABLES, indices):
        clone = int.from_bytes(data[base + IMPORTED_ID * 2:base + IMPORTED_ID * 2 + 2], 'big')
        if clone != index:
            raise ValueError('clone palette entries do not match the selected original')
    dest = PALETTE_BANK + DESTINATION_INDEX * PALETTE_SIZE
    total = 4 * SLOTS * PALETTE_SIZE
    if data[dest:dest + total] != b'\xff' * total:
        raise ValueError('new palette storage is not empty')
    for index in indices[:2]:
        start = PALETTE_BANK + index * PALETTE_SIZE
        if not PALETTE_BANK <= start or start + SLOTS * PALETTE_SIZE > PALETTE_BANK + 0x100000:
            raise ValueError('source palettes are outside the expected bank')
        if start < dest + total and start + SLOTS * PALETTE_SIZE > dest:
            raise ValueError('source palettes overlap new storage')
    result = bytearray(data)
    for variant in range(4):
        start = PALETTE_BANK + indices[variant % 2] * PALETTE_SIZE
        target = dest + variant * SLOTS * PALETTE_SIZE
        result[target:target + SLOTS * PALETTE_SIZE] = data[start:start + SLOTS * PALETTE_SIZE]
        direction = (1, -1, -1, 1)[variant]
        for slot in range(SLOTS):
            for colour in range(1, 16):
                pos = target + slot * PALETTE_SIZE + colour * 2
                word = int.from_bytes(result[pos:pos + 2], 'big')
                result[pos:pos + 2] = adjust(word, direction).to_bytes(2, 'big')
        entry = TABLES[variant] + IMPORTED_ID * 2
        result[entry:entry + 2] = (DESTINATION_INDEX + variant * SLOTS).to_bytes(2, 'big')
    with destination.open('xb') as output:
        output.write(result)
    return hashlib.sha256(result).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--sha256', required=True)
    parser.add_argument('--fighter-id', required=True, type=lambda value: int(value, 0))
    args = parser.parse_args()
    try:
        digest = prepare(args.source, args.destination, args.sha256, args.fighter_id)
    except (OSError, ValueError) as error:
        print(f'Cannot prepare rehearsal palettes: {error}', file=sys.stderr)
        return 1
    print(f'Prepared private palette candidates; SHA-256 {digest}. Rendering is not yet verified.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
