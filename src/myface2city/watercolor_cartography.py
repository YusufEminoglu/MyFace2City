# -*- coding: utf-8 -*-
"""Generative Fluid Watercolor Urban Wash & Pigment Bleed Artistic Filter for myface2city."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image


@dataclass
class WatercolorPigmentParams:
    bleed_radius_px: int = 3
    edge_darkening_strength: float = 1.4
    paper_granulation_noise: float = 0.15
    color_palette: tuple[str, str, str] = ("#1e3a8a", "#0d9488", "#f59e0b")  # Indigo, Teal, Amber


@dataclass
class WatercolorArtwork:
    width: int
    height: int
    pigment_layers_count: int
    svg_content: str

    def to_svg(self) -> str:
        return self.svg_content

    def save_svg(self, output_path: str | Path) -> Path:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(self.to_svg(), encoding="utf-8")
        return out


def apply_watercolor_wash_portrait(
    image: Image.Image | str | Path,
    params: WatercolorPigmentParams | None = None,
    grid_step_px: int = 6,
) -> WatercolorArtwork:
    """Generate fluid watercolor pigment washes with soft edge bleeds and paper texture."""
    p = params or WatercolorPigmentParams()

    if not isinstance(image, Image.Image):
        img = Image.open(image).convert("L")
    else:
        img = image.convert("L")

    w, h = img.size
    pixels = img.load()

    blobs = []
    # Base watercolor filter definition with turbulence and displacement map
    filter_def = """  <defs>
    <filter id="watercolor-bleed" x="-20%" y="-20%" width="140%" height="140%">
      <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="4" result="noise" />
      <feDisplacementMap in="SourceGraphic" in2="noise" scale="8" xChannelSelector="R" yChannelSelector="G" result="displaced" />
      <feGaussianBlur stdDeviation="1.5" result="blurred" />
      <feMerge>
        <feMergeNode in="blurred" />
        <feMergeNode in="displaced" opacity="0.6" />
      </feMerge>
    </filter>
  </defs>"""

    for r in range(0, h, grid_step_px):
        for c in range(0, w, grid_step_px):
            val = pixels[c, r] / 255.0
            if val > 0.85:
                continue  # White paper preserved

            radius = max(3.0, (1.0 - val) * grid_step_px * 1.8)
            pal_idx = int((1.0 - val) * len(p.color_palette)) % len(p.color_palette)
            color = p.color_palette[pal_idx]
            opacity = max(0.25, min(0.75, (1.0 - val) * 0.9))

            blobs.append(
                f'<circle cx="{c}" cy="{r}" r="{radius:.1f}" fill="{color}" opacity="{opacity:.2f}" filter="url(#watercolor-bleed)" />'
            )

    joined_blobs = "\n    ".join(blobs)
    svg_str = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect width="100%" height="100%" fill="#fdfbf7" /> <!-- Textured warm cotton paper -->
{filter_def}
  <g id="pigment-washes">
    {joined_blobs}
  </g>
</svg>"""

    return WatercolorArtwork(
        width=w,
        height=h,
        pigment_layers_count=len(blobs),
        svg_content=svg_str,
    )
