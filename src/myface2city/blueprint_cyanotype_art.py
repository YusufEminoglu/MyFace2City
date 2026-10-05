# -*- coding: utf-8 -*-
"""Architectural Cyanotype Blueprint & Sunprint Art Generator for myface2city."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image


@dataclass
class BlueprintGridParams:
    grid_spacing_px: int = 20
    blueprint_bg_hex: str = "#0f2b5c"  # Classic Prussian blue cyanotype
    drafting_line_hex: str = "#93c5fd"  # Chalk cyan drafting line
    frame_border_width_px: int = 15
    title_text: str = "ARCHITECTURAL ELEVATION & SCHEMATIC"


@dataclass
class CyanotypeArtwork:
    width: int
    height: int
    drafting_elements_count: int
    svg_content: str

    def to_svg(self) -> str:
        return self.svg_content

    def save_svg(self, output_path: str | Path) -> Path:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(self.to_svg(), encoding="utf-8")
        return out


def generate_blueprint_portrait(
    image: Image.Image | str | Path,
    params: BlueprintGridParams | None = None,
) -> CyanotypeArtwork:
    """Generate engineering cyanotype architectural schematic with drafting grids and vector outlines."""
    p = params or BlueprintGridParams()

    if not isinstance(image, Image.Image):
        img = Image.open(image).convert("L")
    else:
        img = image.convert("L")

    w, h = img.size
    pixels = img.load()

    elements = []
    elem_count = 0

    # 1. Technical background drafting grid
    for x in range(0, w, p.grid_spacing_px):
        elements.append(
            f'<line x1="{x}" y1="0" x2="{x}" y2="{h}" stroke="#1e3a8a" stroke-width="0.5" stroke-dasharray="2,2" />'
        )
    for y in range(0, h, p.grid_spacing_px):
        elements.append(
            f'<line x1="0" y1="{y}" x2="{w}" y2="{y}" stroke="#1e3a8a" stroke-width="0.5" stroke-dasharray="2,2" />'
        )

    # 2. Extract architectural wireframe edges based on image tone thresholds
    step = 4
    for y in range(0, h - step, step):
        for x in range(0, w - step, step):
            lum = pixels[x, y] / 255.0
            if lum < 0.45:
                # Strong structural line
                elements.append(
                    f'<rect x="{x}" y="{y}" width="{step}" height="{step}" fill="none" stroke="{p.drafting_line_hex}" stroke-width="1.2" />'
                )
                elem_count += 1
            elif lum < 0.75:
                # Fine dimension cross-mark
                cx, cy = x + step / 2.0, y + step / 2.0
                elements.append(
                    f'<line x1="{cx-1.5}" y1="{cy}" x2="{cx+1.5}" y2="{cy}" stroke="#60a5fa" stroke-width="0.8" />'
                )
                elements.append(
                    f'<line x1="{cx}" y1="{cy-1.5}" x2="{cx}" y2="{cy+1.5}" stroke="#60a5fa" stroke-width="0.8" />'
                )
                elem_count += 1

    # 3. Outer border frame and technical title block
    bw = p.frame_border_width_px
    elements.append(
        f'<rect x="{bw}" y="{bw}" width="{w - 2*bw}" height="{h - 2*bw}" fill="none" stroke="#60a5fa" stroke-width="2" />'
    )
    elements.append(
        f'<text x="{bw + 10}" y="{h - bw - 10}" fill="#93c5fd" font-family="monospace" font-size="10" font-weight="bold">{p.title_text}</text>'
    )

    joined_elems = "\n    ".join(elements)
    svg_str = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect width="100%" height="100%" fill="{p.blueprint_bg_hex}" />
  <g id="blueprint-schematics">
    {joined_elems}
  </g>
</svg>"""

    return CyanotypeArtwork(
        width=w,
        height=h,
        drafting_elements_count=elem_count,
        svg_content=svg_str,
    )
