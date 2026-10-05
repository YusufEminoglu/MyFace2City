# -*- coding: utf-8 -*-
"""Synthwave & Cyberpunk Neon Glow Vector Cartography Art Generator for myface2city."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image


@dataclass
class NeonPalette:
    electric_pink: str = "#ff007f"
    laser_cyan: str = "#00f0ff"
    neon_purple: str = "#a855f7"
    bright_yellow: str = "#fde047"
    deep_space_bg: str = "#09090b"


@dataclass
class CyberpunkArtwork:
    width: int
    height: int
    neon_vectors_count: int
    palette: NeonPalette
    svg_content: str

    def to_svg(self) -> str:
        return self.svg_content

    def save_svg(self, output_path: str | Path) -> Path:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(self.to_svg(), encoding="utf-8")
        return out


def generate_cyberpunk_neon_portrait(
    image: Image.Image | str | Path,
    palette: NeonPalette | None = None,
    grid_horizon_ratio: float = 0.65,
) -> CyberpunkArtwork:
    """Generate retro 80s synthwave / cyberpunk neon vector portrait with glowing drop-shadow filters."""
    pal = palette or NeonPalette()

    if not isinstance(image, Image.Image):
        img = Image.open(image).convert("L")
    else:
        img = image.convert("L")

    w, h = img.size
    pixels = img.load()

    neon_nodes = []
    vector_cnt = 0

    # 1. Perspective synthwave grid lines below horizon
    horizon_y = int(h * grid_horizon_ratio)
    for vy in range(horizon_y, h, 8):
        neon_nodes.append(
            f'<line x1="0" y1="{vy}" x2="{w}" y2="{vy}" stroke="{pal.neon_purple}" stroke-width="0.8" opacity="0.6" />'
        )

    # Vanishing perspective lines
    center_x = w / 2.0
    for vx in range(-w, 2 * w, 24):
        neon_nodes.append(
            f'<line x1="{center_x}" y1="{horizon_y}" x2="{vx}" y2="{h}" stroke="{pal.neon_purple}" stroke-width="0.8" opacity="0.4" />'
        )

    # 2. Glowing vector nodes from image tone
    step = 5
    for y in range(0, horizon_y, step):
        for x in range(0, w, step):
            lum = 1.0 - (pixels[x, y] / 255.0)  # Dark features get bright neon emission
            if lum > 0.6:
                # Electric Pink
                neon_nodes.append(
                    f'<circle cx="{x}" cy="{y}" r="2" fill="{pal.electric_pink}" filter="url(#glow)" />'
                )
                vector_cnt += 1
            elif lum > 0.35:
                # Laser Cyan
                neon_nodes.append(
                    f'<circle cx="{x}" cy="{y}" r="1.5" fill="{pal.laser_cyan}" filter="url(#glow)" />'
                )
                vector_cnt += 1

    joined_nodes = "\n    ".join(neon_nodes)
    svg_str = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="2.5" result="blur1" />
      <feGaussianBlur in="SourceGraphic" stdDeviation="5.0" result="blur2" />
      <feMerge>
        <feMergeNode in="blur2" />
        <feMergeNode in="blur1" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>
  <rect width="100%" height="100%" fill="{pal.deep_space_bg}" />
  <g id="cyberpunk-neon-vectors">
    {joined_nodes}
  </g>
</svg>"""

    return CyberpunkArtwork(
        width=w,
        height=h,
        neon_vectors_count=vector_cnt,
        palette=pal,
        svg_content=svg_str,
    )
