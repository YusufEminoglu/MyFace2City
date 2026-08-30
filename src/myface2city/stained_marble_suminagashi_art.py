# -*- coding: utf-8 -*-
"""Japanese Suminagashi Water Marbling & Swirling Ink Art Generator for myface2city."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Sequence
from PIL import Image


@dataclass
class MarblingVortexParams:
    vortex_intensity: float = 1.4
    num_ink_ripples: int = 16
    ink_color_hex: str = "#1a2a3a"  # Deep Indigo
    paper_water_hex: str = "#fdfbf7"


@dataclass
class SuminagashiArtwork:
    width: int
    height: int
    ink_streamlines_count: int
    marbled_vortices_count: int
    svg_data: str

    def to_svg(self) -> str:
        return self.svg_data

    def save_svg(self, path: str | Path) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(self.svg_data, encoding="utf-8")


def generate_suminagashi_marbling_portrait(
    image: Image.Image,
    params: MarblingVortexParams | None = None,
    grid_step_px: int = 5,
) -> SuminagashiArtwork:
    """Generate Japanese Suminagashi floating ink marbling art with hydrodynamic vortex streamlines."""
    p = params or MarblingVortexParams()
    img = image.convert("L")
    w, h = img.size

    svg_elements: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
        f'  <rect width="{w}" height="{h}" fill="{p.paper_water_hex}" />',
        '  <!-- Suminagashi Marbled Ink Veins -->',
        f'  <g stroke="{p.ink_color_hex}" fill="none" stroke-linecap="round">',
    ]

    streamlines = 0
    vortices = 0

    cx, cy = w / 2.0, h / 2.0

    for y in range(0, h, grid_step_px):
        path_pts: list[str] = []
        for x in range(0, w, grid_step_px):
            lum = img.getpixel((x, y))
            # Hydrodynamic swirl displacement
            dx = x - cx
            dy = y - cy
            dist = math.hypot(dx, dy)
            angle = math.atan2(dy, dx)

            # Vortex swirl angle offset
            swirl = angle + (dist / 30.0) * p.vortex_intensity * ((255 - lum) / 255.0)
            sx = cx + dist * math.cos(swirl)
            sy = cy + dist * math.sin(swirl)

            stroke_w = max(0.4, min(2.5, ((255 - lum) / 255.0) * 2.2))

            if len(path_pts) == 0:
                path_pts.append(f"M {sx:.1f} {sy:.1f}")
            else:
                path_pts.append(f"L {sx:.1f} {sy:.1f}")

        if len(path_pts) > 1:
            d_str = " ".join(path_pts)
            svg_elements.append(f'    <path d="{d_str}" stroke-width="0.8" opacity="0.75" />')
            streamlines += 1

    vortices = max(1, int(p.vortex_intensity * 3))
    svg_elements.append('  </g>')
    svg_elements.append('</svg>')

    return SuminagashiArtwork(
        width=w,
        height=h,
        ink_streamlines_count=streamlines,
        marbled_vortices_count=vortices,
        svg_data="\n".join(svg_elements),
    )
