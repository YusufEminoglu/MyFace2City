# -*- coding: utf-8 -*-
"""Classical Error Diffusion (Floyd-Steinberg/Atkinson) & Bayer Ordered Dithering for myface2city."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image

BAYER_4X4 = [
    [0 / 16.0, 8 / 16.0, 2 / 16.0, 10 / 16.0],
    [12 / 16.0, 4 / 16.0, 14 / 16.0, 6 / 16.0],
    [3 / 16.0, 11 / 16.0, 1 / 16.0, 9 / 16.0],
    [15 / 16.0, 7 / 16.0, 13 / 16.0, 5 / 16.0],
]


@dataclass
class DitherArtwork:
    """1-bit monochrome dithered portrait bitmap."""

    width: int
    height: int
    dither_algorithm: str
    dither_matrix: list[list[int]]  # 0 or 255

    def to_image(self) -> Image.Image:
        img = Image.new("1", (self.width, self.height))
        pixels = img.load()
        for r in range(self.height):
            for c in range(self.width):
                pixels[c, r] = 1 if self.dither_matrix[r][c] > 128 else 0
        return img


def generate_ordered_dither_portrait(
    image: Image.Image | str | Path,
    scale_factor: float = 1.0,
) -> DitherArtwork:
    """Apply Bayer 4x4 ordered matrix threshold dithering to portrait image."""
    if not isinstance(image, Image.Image):
        img = Image.open(image).convert("L")
    else:
        img = image.convert("L")

    if scale_factor != 1.0:
        nw = max(1, int(img.width * scale_factor))
        nh = max(1, int(img.height * scale_factor))
        img = img.resize((nw, nh), Image.Resampling.BILINEAR)

    w, h = img.size
    pixels = img.load()
    matrix = [[0] * w for _ in range(h)]

    for r in range(h):
        for c in range(w):
            val = pixels[c, r] / 255.0
            threshold = BAYER_4X4[r % 4][c % 4]
            matrix[r][c] = 255 if val > threshold else 0

    return DitherArtwork(width=w, height=h, dither_algorithm="Bayer_4x4", dither_matrix=matrix)


def apply_error_diffusion_dither(
    image: Image.Image | str | Path,
    method: str = "floyd_steinberg",  # 'floyd_steinberg' or 'atkinson'
) -> DitherArtwork:
    """Apply Floyd-Steinberg or Atkinson error diffusion spatial halftoning."""
    if not isinstance(image, Image.Image):
        img = Image.open(image).convert("L")
    else:
        img = image.convert("L")

    w, h = img.size
    pixels = img.load()

    # Float buffer for error accumulation
    buf = [[float(pixels[c, r]) for c in range(w)] for r in range(h)]
    out_matrix = [[0] * w for _ in range(h)]

    is_atkinson = method.lower() == "atkinson"

    for r in range(h):
        for c in range(w):
            old_val = buf[r][c]
            new_val = 255.0 if old_val >= 128.0 else 0.0
            out_matrix[r][c] = int(new_val)
            err = old_val - new_val

            if is_atkinson:
                # Atkinson distributes 1/8 to 6 surrounding pixels
                diff_weight = err / 8.0
                coords = [(r, c + 1), (r, c + 2), (r + 1, c - 1), (r + 1, c), (r + 1, c + 1), (r + 2, c)]
                for nr, nc in coords:
                    if 0 <= nr < h and 0 <= nc < w:
                        buf[nr][nc] += diff_weight
            else:
                # Floyd-Steinberg: (r, c+1) = 7/16, (r+1, c-1) = 3/16, (r+1, c) = 5/16, (r+1, c+1) = 1/16
                if c + 1 < w:
                    buf[r][c + 1] += err * (7.0 / 16.0)
                if r + 1 < h:
                    if c - 1 >= 0:
                        buf[r + 1][c - 1] += err * (3.0 / 16.0)
                    buf[r + 1][c] += err * (5.0 / 16.0)
                    if c + 1 < w:
                        buf[r + 1][c + 1] += err * (1.0 / 16.0)

    return DitherArtwork(width=w, height=h, dither_algorithm=method, dither_matrix=out_matrix)
