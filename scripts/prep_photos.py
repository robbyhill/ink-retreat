"""Resize photos and strip metadata for the countdown background.

Usage:
    python3 scripts/prep_photos.py ~/Desktop/ink_photos ~/code/ink-retreat-photos/photos

    python3 scripts/prep_photos.py ~/Desktop/finale.jpeg ~/code/ink-retreat-photos/finale/finale.jpg

Each output file gets a random name (or the given name, for a single file),
is at most 1600px on its long edge, and is re-encoded without EXIF/GPS data.
"""

import secrets
import sys
from pathlib import Path

from PIL import Image, ImageOps

MAX_EDGE = 1600
QUALITY = 80
EXTS = {".jpg", ".jpeg", ".png", ".heic"}


def prep(src: Path, out: Path) -> None:
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)  # bake in rotation before dropping EXIF
        im = im.convert("RGB")
        im.thumbnail((MAX_EDGE, MAX_EDGE))
        im.save(out, "JPEG", quality=QUALITY, optimize=True, progressive=True)


def main(src: Path, dst: Path) -> None:
    if src.is_file():
        dst.parent.mkdir(parents=True, exist_ok=True)
        prep(src, dst)
        print(f"Wrote {dst}")
        return
    dst.mkdir(parents=True, exist_ok=True)
    files = sorted(p for p in src.iterdir() if p.suffix.lower() in EXTS)
    for p in files:
        prep(p, dst / f"{secrets.token_hex(6)}.jpg")
    print(f"Wrote {len(files)} photos to {dst}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(Path(sys.argv[1]).expanduser(), Path(sys.argv[2]).expanduser())
