"""Copy prepared local game files into a separate, private experiment folder."""
import argparse
import shutil
import sys
from pathlib import Path


PRIVATE = Path(__file__).resolve().parents[3] / "private"
REQUIRED = ("271-pd.bin", "sp-s2.sp1")


def prepare(source, destination):
    private = PRIVATE.resolve(strict=True)
    source = source.resolve(strict=True)
    destination = destination.resolve()
    if not source.is_relative_to(private) or not destination.is_relative_to(private):
        raise ValueError("source and destination must be inside private/")
    if not source.is_dir() or any(not (source / name).is_file() for name in REQUIRED):
        raise ValueError("source must contain the prepared program and BIOS")
    if destination.exists() or destination.is_relative_to(source):
        raise ValueError("destination must be a new directory outside the source")
    if any(path.is_symlink() or not path.resolve().is_relative_to(source)
           for path in source.rglob("*")):
        raise ValueError("source must not contain links outside the source")
    shutil.copytree(source, destination)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    try:
        prepare(args.source, args.destination)
    except (OSError, ValueError) as error:
        print(f"Preparation failed: {error}", file=sys.stderr)
        return 1
    print(f"Prepared an independent copy in {args.destination}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
