# -*- coding: utf-8 -*-
"""FLIR Thermal Infrared Heatmap & False-Color Spectrum Art for myface2city."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image


@dataclass
class FLIRPalette:
    # Classic Ironbow thermal color lookup (from cold to hot)
    ironbow_hex: list[str] = field(
        default_factory=lambda: [
            "#000004",  # Deep cold black/purple
            "#1b0c41",  # Dark indigo
            "#4a0c6b",  # Purple
            "#781c6d",  # Magenta
            "#a52c60",  # Crimson
            "#cf4446",  # Red-orange
            "#ed6925",  # Orange
            "#fb9b06",  # Amber yellow
            "#f7d13d",  # Bright yellow
            "#fcffa4",  # Hot incandescent white
        ]
    )


@dataclass
class ThermalInfraredArtwork:
    width: int
    height: int
    min_temperature_c: float
    max_temperature_c: float
    isotherms_count: int
    svg_data: str

    def to_svg(self) -> str:
        return self.svg_data

    def save_svg(self, path: str | Path) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(self.svg_data, encoding="utf-8")


def generate_thermal_infrared_portrait(
    image: Image.Image,
    min_temp_c: float = 24.0,  # Ambient skin background
    max_temp_c: float = 37.5,  # Peak facial vascular temperature
    palette: FLIRPalette | None = None,
    pixel_bin_size_px: int = 2,
) -> ThermalInfraredArtwork:
    """Map portrait luminescence to FLIR radiometric thermal false-color infrared spectral bands."""
    pal = palette or FLIRPalette()
    img = image.convert("L")
    w, h = img.size

    num_colors = len(pal.ironbow_hex)
    svg_elements: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
        f'  <rect width="{w}" height="{h}" fill="{pal.ironbow_hex[0]}" />',
        '  <g id="flir-thermal-infrared">',
    ]

    isotherm_count = 0

    for y in range(0, h, pixel_bin_size_px):
        for x in range(0, w, pixel_bin_size_px):
            lum = img.getpixel((x, y))
            frac = lum / 255.0
            idx = min(num_colors - 1, int(frac * num_colors))
            color = pal.ironbow_hex[idx]
            isotherm_count += 1

            bw = min(pixel_bin_size_px, w - x)
            bh = min(pixel_bin_size_px, h - y)

            svg_elements.append(
                f'    <rect x="{x}" y="{y}" width="{bw}" height="{bh}" fill="{color}" />'
            )

    svg_elements.append("  </g>")
    svg_elements.append("</svg>")

    return ThermalInfraredArtwork(
        width=w,
        height=h,
        min_temperature_c=min_temp_c,
        max_temperature_c=max_temp_c,
        isotherms_count=isotherm_count,
        svg_data="\n".join(svg_elements),
    )
