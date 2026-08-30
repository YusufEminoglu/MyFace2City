# -*- coding: utf-8 -*-
"""Vintage Dual-Color Risograph Print & Stipple Screen Art Generator for myface2city."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Sequence
from PIL import Image


@dataclass
class RisoColorDrum:
    name: str = "Fluorescent Pink"
    hex_code: str = "#ff48b0"
    screen_angle_deg: float = 15.0
    misregistration_offset_px: tuple[float, float] = (1.5, -1.0)


@dataclass
class RisographArtwork:
    width: int
    height: int
    drum_1_dots_count: int
    drum_2_dots_count: int
    svg_data: str

    def to_svg(self) -> str:
        return self.svg_data

    def save_svg(self, path: str | Path) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(self.svg_data, encoding="utf-8")


def generate_risograph_print_portrait(
    image: Image.Image,
    dot_pitch_px: int = 4,
    drum_1: RisoColorDrum | None = None,
    drum_2: RisoColorDrum | None = None,
    paper_tone_hex: str = "#faf6ed",
) -> RisographArtwork:
    """Generate dual-color Risograph screen print with organic stencil halftone dots and misregistration offsets."""
    d1 = drum_1 or RisoColorDrum("Fluorescent Pink", "#ff48b0", 15.0, (1.2, -0.8))
    d2 = drum_2 or RisoColorDrum("Medium Blue", "#0078bf", 75.0, (-0.8, 1.2))

    img = image.convert("L")
    w, h = img.size

    svg_elements: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
        f'  <rect width="{w}" height="{h}" fill="{paper_tone_hex}" />',
        f'  <!-- Risograph Drum 1: {d1.name} -->',
        f'  <g id="riso-drum-1" fill="{d1.hex_code}" opacity="0.82" style="mix-blend-mode: multiply;">',
    ]

    dots1 = 0
    dots2 = 0

    # Drum 1 pass (Highlights / Midtones)
    for y in range(0, h, dot_pitch_px):
        for x in range(0, w, dot_pitch_px):
            lum = img.getpixel((x, y))
            if lum < 220:  # Inked area
                r = max(0.5, ((255 - lum) / 255.0) * (dot_pitch_px * 0.55))
                cx = x + d1.misregistration_offset_px[0]
                cy = y + d1.misregistration_offset_px[1]
                svg_elements.append(f'    <circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.2f}" />')
                dots1 += 1

    svg_elements.append("  </g>")
    svg_elements.append(f'  <!-- Risograph Drum 2: {d2.name} -->')
    svg_elements.append(f'  <g id="riso-drum-2" fill="{d2.hex_code}" opacity="0.82" style="mix-blend-mode: multiply;">')

    # Drum 2 pass (Shadows / Deep tones)
    for y in range(0, h, dot_pitch_px):
        for x in range(0, w, dot_pitch_px):
            lum = img.getpixel((x, y))
            if lum < 140:  # Dark shadow areas
                r = max(0.6, ((140 - lum) / 140.0) * (dot_pitch_px * 0.65))
                cx = x + d2.misregistration_offset_px[0]
                cy = y + d2.misregistration_offset_px[1]
                svg_elements.append(f'    <circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.2f}" />')
                dots2 += 1

    svg_elements.append("  </g>")
    svg_elements.append("</svg>")

    return RisographArtwork(
        width=w,
        height=h,
        drum_1_dots_count=dots1,
        drum_2_dots_count=dots2,
        svg_data="\n".join(svg_elements),
    )
