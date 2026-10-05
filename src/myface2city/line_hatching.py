# -*- coding: utf-8 -*-
"""Architectural & Copperplate Cross-Hatching Line Engraver for myface2city."""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from PIL import Image


@dataclass
class HatchingStroke:
    x1: float
    y1: float
    x2: float
    y2: float
    stroke_width: float = 1.0


@dataclass
class HatchingArtwork:
    """Architectural engraved cross-hatching artwork."""

    width: int
    height: int
    strokes: list[HatchingStroke]

    def to_svg(self, stroke_color: str = "#0f172a", background_color: str = "#f8fafc") -> str:
        lines = [
            f'<line x1="{s.x1:.2f}" y1="{s.y1:.2f}" x2="{s.x2:.2f}" y2="{s.y2:.2f}" stroke="{stroke_color}" stroke-width="{s.stroke_width:.2f}" stroke-linecap="round" />'
            for s in self.strokes
        ]
        joined = "\n  ".join(lines)
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" width="{self.width}" height="{self.height}">
  <rect width="100%" height="100%" fill="{background_color}" />
  {joined}
</svg>"""

    def save_svg(self, output_path: str | Path) -> Path:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(self.to_svg(), encoding="utf-8")
        return out


def generate_engraved_hatching_art(
    image: Image.Image | str | Path,
    grid_step_px: int = 6,
    hatch_angles_deg: Sequence[float] = (45.0, -45.0, 0.0),
    luminance_thresholds: Sequence[float] = (0.75, 0.50, 0.25),
) -> HatchingArtwork:
    """Generate multi-pass pen & ink cross-hatching lines modulated by portrait tone."""
    if not isinstance(image, Image.Image):
        img = Image.open(image).convert("L")
    else:
        img = image.convert("L")

    w, h = img.size
    pixels = img.load()
    strokes: list[HatchingStroke] = []

    # Iterate over sampling grid
    for r in range(0, h, grid_step_px):
        for c in range(0, w, grid_step_px):
            val = pixels[c, r] / 255.0  # 0.0 (dark) to 1.0 (light)

            # Determine number of cross-hatch passes
            passes = 0
            for thresh in luminance_thresholds:
                if val <= thresh:
                    passes += 1

            for p in range(passes):
                ang = hatch_angles_deg[p % len(hatch_angles_deg)]
                rad = math.radians(ang)
                half_len = (grid_step_px * 0.7)

                dx = half_len * math.cos(rad)
                dy = half_len * math.sin(rad)

                strokes.append(
                    HatchingStroke(
                        x1=c - dx,
                        y1=r - dy,
                        x2=c + dx,
                        y2=r + dy,
                        stroke_width=max(0.6, 1.4 - val),
                    )
                )

    return HatchingArtwork(width=w, height=h, strokes=strokes)
