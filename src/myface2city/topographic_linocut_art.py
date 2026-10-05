# -*- coding: utf-8 -*-
"""Relief Linocut & Woodblock Topographic Print Art Generator for myface2city."""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

from PIL import Image


@dataclass
class LinocutCarveParams:
    line_spacing_px: int = 5
    contour_intervals: int = 8
    ink_color_hex: str = "#18181b"  # Deep relief printer's ink black
    paper_color_hex: str = "#fef08a"  # Warm Japanese washi paper yellow
    carve_angle_degrees: float = 25.0


@dataclass
class LinocutArtwork:
    width: int
    height: int
    groove_count: int
    svg_content: str

    def to_svg(self) -> str:
        return self.svg_content

    def save_svg(self, output_path: str | Path) -> Path:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(self.to_svg(), encoding="utf-8")
        return out


def generate_linocut_portrait(
    image: Image.Image | str | Path,
    params: LinocutCarveParams | None = None,
) -> LinocutArtwork:
    """Generate Japanese Moku-Hanga / Western Linocut woodblock relief print from tone levels."""
    p = params or LinocutCarveParams()

    if not isinstance(image, Image.Image):
        img = Image.open(image).convert("L")
    else:
        img = image.convert("L")

    w, h = img.size
    pixels = img.load()

    paths = []
    groove_cnt = 0

    rad = math.radians(p.carve_angle_degrees)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    # Sweep parallel cutting passes across canvas
    diag = int(math.hypot(w, h))
    for offset in range(-diag, diag, p.line_spacing_px):
        current_stroke = []
        for d in range(0, diag, 3):
            # Transform line coordinate to canvas (x, y)
            x = int(offset * cos_a - d * sin_a + w / 2.0)
            y = int(offset * sin_a + d * cos_a + h / 2.0)

            if 0 <= x < w and 0 <= y < h:
                lum = pixels[x, y] / 255.0  # 0.0 (dark) to 1.0 (bright)
                # In linocut, white areas are carved away with wide gouges; dark areas retain ink
                stroke_w = max(0.5, (1.0 - lum) * (p.line_spacing_px * 0.9))
                current_stroke.append((x, y, stroke_w))

        if len(current_stroke) >= 2:
            # Construct SVG polyline chunks
            pts_str = " ".join(f"{pt[0]},{pt[1]}" for pt in current_stroke)
            avg_w = sum(pt[2] for pt in current_stroke) / len(current_stroke)
            if avg_w > 0.8:
                paths.append(
                    f'<polyline points="{pts_str}" fill="none" stroke="{p.ink_color_hex}" stroke-width="{avg_w:.2f}" stroke-linecap="round" />'
                )
                groove_cnt += 1

    joined_paths = "\n  ".join(paths)
    svg_str = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect width="100%" height="100%" fill="{p.paper_color_hex}" />
  <g id="linocut-grooves">
  {joined_paths}
  </g>
</svg>"""

    return LinocutArtwork(
        width=w,
        height=h,
        groove_count=groove_cnt,
        svg_content=svg_str,
    )
