# -*- coding: utf-8 -*-
"""Cathedral Stained Glass Mosaic & Lead Came Art Generator for myface2city."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image


@dataclass
class GlassFacet:
    cell_id: str
    polygon_vertices: list[tuple[float, float]]
    glass_color_hex: str
    translucency_opacity: float


@dataclass
class StainedGlassArtwork:
    width: int
    height: int
    facets_count: int
    facets: list[GlassFacet]
    svg_content: str

    def to_svg(self) -> str:
        return self.svg_content

    def save_svg(self, output_path: str | Path) -> Path:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(self.to_svg(), encoding="utf-8")
        return out


def generate_stained_glass_portrait(
    image: Image.Image | str | Path,
    tile_size_px: int = 12,
    lead_came_width_px: float = 2.5,
    glass_palette: tuple[str, ...] = ("#1e3a8a", "#b91c1c", "#f59e0b", "#047857", "#6d28d9", "#fcd34d"),
) -> StainedGlassArtwork:
    """Generate illuminated cathedral stained glass mosaic with thick black lead cames dividing luminous facets."""
    if not isinstance(image, Image.Image):
        img = Image.open(image).convert("L")
    else:
        img = image.convert("L")

    w, h = img.size
    pixels = img.load()

    facets: list[GlassFacet] = []
    polys = []

    tile_idx = 1
    for r in range(0, h, tile_size_px):
        for c in range(0, w, tile_size_px):
            tw = min(tile_size_px, w - c)
            th = min(tile_size_px, h - r)

            # Sample average tone in tile
            sample_x = min(w - 1, c + tw // 2)
            sample_y = min(h - 1, r + th // 2)
            lum = 1.0 - (pixels[sample_x, sample_y] / 255.0)  # darker = richer color

            pal_idx = int(lum * len(glass_palette)) % len(glass_palette)
            color = glass_palette[pal_idx]
            opacity = max(0.6, min(1.0, 0.4 + lum * 0.6))

            # Add jitter to tile corners for organic cut glass look
            jitter_seed = (c * 31 + r * 17) % 7 - 3
            v1 = (float(c), float(r))
            v2 = (float(c + tw), float(r + (jitter_seed * 0.3)))
            v3 = (float(c + tw + (jitter_seed * 0.3)), float(r + th))
            v4 = (float(c), float(r + th))

            facet_verts = [v1, v2, v3, v4]
            facets.append(
                GlassFacet(
                    cell_id=f"facet_{tile_idx}",
                    polygon_vertices=facet_verts,
                    glass_color_hex=color,
                    translucency_opacity=opacity,
                )
            )

            pts_str = f"{v1[0]:.1f},{v1[1]:.1f} {v2[0]:.1f},{v2[1]:.1f} {v3[0]:.1f},{v3[1]:.1f} {v4[0]:.1f},{v4[1]:.1f}"
            polys.append(
                f'<polygon points="{pts_str}" fill="{color}" fill-opacity="{opacity:.2f}" stroke="#0f172a" stroke-width="{lead_came_width_px:.1f}" stroke-linejoin="round" />'
            )
            tile_idx += 1

    joined_polys = "\n    ".join(polys)
    svg_str = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect width="100%" height="100%" fill="#020617" />
  <g id="stained-glass-mosaic">
    {joined_polys}
  </g>
</svg>"""

    return StainedGlassArtwork(
        width=w,
        height=h,
        facets_count=len(facets),
        facets=facets,
        svg_content=svg_str,
    )
