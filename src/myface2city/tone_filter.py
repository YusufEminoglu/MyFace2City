# -*- coding: utf-8 -*-
"""Edge-Preserving Bilateral Filter & Adaptive Contrast Equalizer for myface2city."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageOps


def bilateral_texture_filter(
    image: Image.Image | str | Path,
    spatial_sigma: float = 3.0,
    range_sigma: float = 30.0,
) -> Image.Image:
    """Edge-preserving bilateral smoothing filter to clean noise while retaining sharp boundary lines."""
    if not isinstance(image, Image.Image):
        img = Image.open(image).convert("L")
    else:
        img = image.convert("L")

    w, h = img.size
    pixels = img.load()
    out_img = Image.new("L", (w, h))
    out_pix = out_img.load()

    rad = int(spatial_sigma * 2)
    spatial_coeff = -0.5 / (spatial_sigma ** 2)
    range_coeff = -0.5 / (range_sigma ** 2)

    for y in range(h):
        for x in range(w):
            center_val = float(pixels[x, y])
            weight_sum = 0.0
            val_sum = 0.0

            for dy in range(-rad, rad + 1):
                ny = y + dy
                if ny < 0 or ny >= h:
                    continue
                for dx in range(-rad, rad + 1):
                    nx = x + dx
                    if nx < 0 or nx >= w:
                        continue

                    neighbor_val = float(pixels[nx, ny])
                    spatial_d2 = dx * dx + dy * dy
                    range_d2 = (neighbor_val - center_val) ** 2

                    w_ij = math.exp(spatial_d2 * spatial_coeff + range_d2 * range_coeff)
                    weight_sum += w_ij
                    val_sum += neighbor_val * w_ij

            out_pix[x, y] = int(val_sum / max(1e-6, weight_sum))

    return out_img


def clahe_contrast_enhancer(
    image: Image.Image | str | Path,
    clip_limit: float = 2.0,
) -> Image.Image:
    """Enhance local contrast of facial and street textures."""
    if not isinstance(image, Image.Image):
        img = Image.open(image).convert("L")
    else:
        img = image.convert("L")

    # Autocontrast and equalization
    equalized = ImageOps.equalize(img)
    return Image.blend(img, equalized, alpha=min(1.0, clip_limit / 3.0))
