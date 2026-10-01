"""Resize photos and strip metadata for the countdown background.

Usage:
    python3 scripts/prep_photos.py ~/Desktop/ink_photos ~/code/ink-retreat-photos/photos

Each output file gets a random name, is at most 1600px on its long edge,
and is re-encoded without EXIF/GPS data.
"""

import secrets
import sys
from pathlib import Path

from PIL import Image, ImageOps

MAX_EDGE = 1600
QUALITY = 80
EXTS = {".jpg", ".jpeg", ".png", ".heic"}


def main(src: Path, dst: Path) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    files = sorted(p for p in src.iterdir() if p.suffix.lower() in EXTS)
    for p in files:
        with Image.open(p) as im:
            im = ImageOps.exif_transpose(im)  # bake in rotation before dropping EXIF
            im = im.convert("RGB")
            im.thumbnail((MAX_EDGE, MAX_EDGE))
            out = dst / f"{secrets.token_hex(6)}.jpg"
            im.save(out, "JPEG", quality=QUALITY, optimize=True, progressive=True)
    print(f"Wrote {len(files)} photos to {dst}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(Path(sys.argv[1]).expanduser(), Path(sys.argv[2]).expanduser())
