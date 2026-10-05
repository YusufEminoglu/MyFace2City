# -*- coding: utf-8 -*-
"""Faceted Origami Papercraft & Low-Poly Tessellation Art Generator for myface2city."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image


@dataclass
class PaperFacetMesh:
    facet_id: str
    vertices_2d: list[tuple[float, float]]
    fill_color_hex: str
    crease_shadow_factor: float


@dataclass
class OrigamiArtwork:
    width: int
    height: int
    facets_count: int
    paper_creases_count: int
    svg_data: str

    def to_svg(self) -> str:
        return self.svg_data

    def save_svg(self, path: str | Path) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(self.svg_data, encoding="utf-8")


def generate_origami_papercraft_portrait(
    image: Image.Image,
    grid_subdivision_px: int = 6,
    paper_base_color_hex: str = "#f0ebe1",
) -> OrigamiArtwork:
    """Generate 3D folded low-poly origami papercraft tessellation with directional facet shading."""
    img = image.convert("L")
    w, h = img.size

    svg_elements: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
        f'  <rect width="{w}" height="{h}" fill="{paper_base_color_hex}" />',
        '  <g id="origami-papercraft-mesh">',
    ]

    facet_id = 0

    for y in range(0, h - grid_subdivision_px, grid_subdivision_px):
        for x in range(0, w - grid_subdivision_px, grid_subdivision_px):
            # Compute quadrant luminance
            lum_tl = img.getpixel((x, y))
            lum_br = img.getpixel((x + grid_subdivision_px, y + grid_subdivision_px))

            # Triangle 1: (x,y), (x+step, y), (x, y+step)
            t1_lum = lum_tl
            t1_hex = f"#{int(t1_lum):02x}{int(t1_lum * 0.95):02x}{int(t1_lum * 0.90):02x}"
            pts1 = f"{x},{y} {x+grid_subdivision_px},{y} {x},{y+grid_subdivision_px}"
            svg_elements.append(
                f'    <polygon points="{pts1}" fill="{t1_hex}" stroke="#b0a89a" stroke-width="0.3" />'
            )

            # Triangle 2: (x+step, y), (x+step, y+step), (x, y+step)
            t2_lum = lum_br
            t2_hex = f"#{int(t2_lum):02x}{int(t2_lum * 0.95):02x}{int(t2_lum * 0.90):02x}"
            pts2 = f"{x+grid_subdivision_px},{y} {x+grid_subdivision_px},{y+grid_subdivision_px} {x},{y+grid_subdivision_px}"
            svg_elements.append(
                f'    <polygon points="{pts2}" fill="{t2_hex}" stroke="#b0a89a" stroke-width="0.3" />'
            )

            facet_id += 2

    svg_elements.append("  </g>")
    svg_elements.append("</svg>")

    return OrigamiArtwork(
        width=w,
        height=h,
        facets_count=facet_id,
        paper_creases_count=facet_id * 2,
        svg_data="\n".join(svg_elements),
    )
