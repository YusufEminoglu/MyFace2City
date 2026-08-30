# -*- coding: utf-8 -*-
"""Artisan Marquetry Wood Inlay & Parquet Geometric Mosaic Generator for myface2city."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Sequence
from PIL import Image


@dataclass
class WoodSpeciesPalette:
    # Wood species from lightest to darkest
    palette_hex: list[str] = field(
        default_factory=lambda: [
            "#fdf5e6",  # Bleached Maple
            "#eed9b3",  # White Oak
            "#d2a679",  # American Birch
            "#a06535",  # Cherry Wood
            "#6e3d1d",  # Black Walnut
            "#3d1f0d",  # African Ebony
        ]
    )


@dataclass
class MarquetryArtwork:
    width: int
    height: int
    parquet_tiles_count: int
    wood_species_distribution: dict[str, int]
    svg_data: str

    def to_svg(self) -> str:
        return self.svg_data

    def save_svg(self, path: str | Path) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(self.svg_data, encoding="utf-8")


def generate_marquetry_portrait(
    image: Image.Image,
    tile_size_px: int = 4,
    palette: WoodSpeciesPalette | None = None,
) -> MarquetryArtwork:
    """Generate fine woodworking marquetry inlay portrait using natural wood grain tonal bins."""
    pal = palette or WoodSpeciesPalette()
    img = image.convert("L")
    w, h = img.size

    num_bins = len(pal.palette_hex)
    bin_size = 256.0 / float(num_bins)

    distrib: dict[str, int] = {c: 0 for c in pal.palette_hex}
    svg_elements: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
        f'  <rect width="{w}" height="{h}" fill="{pal.palette_hex[0]}" />',
        '  <g id="marquetry-wood-inlay">',
    ]

    tile_count = 0

    for y in range(0, h, tile_size_px):
        for x in range(0, w, tile_size_px):
            # Compute average luminance in tile
            tot = 0
            cnt = 0
            for dy in range(tile_size_px):
                for dx in range(tile_size_px):
                    if x + dx < w and y + dy < h:
                        tot += img.getpixel((x + dx, y + dy))
                        cnt += 1
            avg_lum = tot / max(1, cnt)

            # Invert: darker image pixel -> darker exotic wood
            inv_lum = 255 - avg_lum
            bin_idx = min(num_bins - 1, int(inv_lum // bin_size))
            wood_color = pal.palette_hex[bin_idx]
            distrib[wood_color] += 1
            tile_count += 1

            tw = min(tile_size_px, w - x)
            th = min(tile_size_px, h - y)

            # Subtle wood grain angle rotation pattern
            grain_rot = ((x // tile_size_px + y // tile_size_px) % 2) * 90
            svg_elements.append(
                f'    <rect x="{x}" y="{y}" width="{tw}" height="{th}" fill="{wood_color}" stroke="#221105" stroke-width="0.3" opacity="0.95" />'
            )

    svg_elements.append("  </g>")
    svg_elements.append("</svg>")

    return MarquetryArtwork(
        width=w,
        height=h,
        parquet_tiles_count=tile_count,
        wood_species_distribution=distrib,
        svg_data="\n".join(svg_elements),
    )
