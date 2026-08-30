# -*- coding: utf-8 -*-
"""Flow-Field Vector Streamline Portrait Art Generator for myface2city."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Sequence
from PIL import Image, ImageFilter


@dataclass
class Streamline:
    """A single continuous vector flow line."""

    points: list[tuple[float, float]]
    stroke_width: float
    color_hex: str


@dataclass
class FlowFieldArtwork:
    """Master generative flow field artwork."""

    width: int
    height: int
    streamlines: list[Streamline]

    def to_svg(self, stroke_color: str | None = None, background: str = "#0f172a") -> str:
        paths = []
        for line in self.streamlines:
            if len(line.points) < 2:
                continue
            d = f"M {line.points[0][0]:.2f} {line.points[0][1]:.2f} " + " ".join(
                f"L {p[0]:.2f} {p[1]:.2f}" for p in line.points[1:]
            )
            col = stroke_color or line.color_hex
            paths.append(
                f'<path d="{d}" stroke="{col}" stroke-width="{line.stroke_width:.2f}" fill="none" stroke-linecap="round" stroke-linejoin="round" />'
            )

        joined_paths = "\n  ".join(paths)
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" width="{self.width}" height="{self.height}">
  <rect width="100%" height="100%" fill="{background}" />
  {joined_paths}
</svg>"""

    def save_svg(self, output_path: str | Path) -> Path:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(self.to_svg(), encoding="utf-8")
        return out


def generate_flow_field_art(
    image: Image.Image | str | Path,
    num_particles: int = 1500,
    step_length: float = 3.0,
    max_steps: int = 40,
    noise_scale: float = 0.02,
) -> FlowFieldArtwork:
    """Trace curvilinear vector streamlines guided by image luminance & edge gradients."""
    if not isinstance(image, Image.Image):
        img = Image.open(image).convert("L")
    else:
        img = image.convert("L")

    w, h = img.size
    pixels = img.load()

    # Compute horizontal and vertical gradients
    img_blur = img.filter(ImageFilter.GaussianBlur(radius=1.5))
    blur_pix = img_blur.load()

    def get_angle(x: float, y: float) -> float:
        ix = max(1, min(w - 2, int(x)))
        iy = max(1, min(h - 2, int(y)))
        # Sobel/gradient
        gx = (int(blur_pix[ix + 1, iy]) - int(blur_pix[ix - 1, iy])) / 2.0
        gy = (int(blur_pix[ix, iy + 1]) - int(blur_pix[ix, iy - 1])) / 2.0
        # Flow is perpendicular to gradient
        ang = math.atan2(-gx, gy)
        # Add subtle swirl
        ang += math.sin(x * noise_scale) * math.cos(y * noise_scale) * 0.5
        return ang

    streamlines: list[Streamline] = []
    rng = random.Random(42)

    for _ in range(num_particles):
        px = rng.uniform(0, w)
        py = rng.uniform(0, h)
        pts = [(px, py)]

        lum = float(pixels[int(px), int(py)]) / 255.0  # 0=dark, 1=bright
        # Darker areas get thicker strokes
        stroke_w = max(0.5, (1.0 - lum) * 2.5 + 0.3)
        # Opacity / brightness
        shade = int(lum * 200 + 55)
        color = f"#{shade:02x}{shade:02x}{shade:02x}"

        curr_x, curr_y = px, py
        for _ in range(max_steps):
            ang = get_angle(curr_x, curr_y)
            curr_x += step_length * math.cos(ang)
            curr_y += step_length * math.sin(ang)

            if curr_x < 0 or curr_x >= w or curr_y < 0 or curr_y >= h:
                break
            pts.append((curr_x, curr_y))

        if len(pts) >= 3:
            streamlines.append(Streamline(points=pts, stroke_width=stroke_w, color_hex=color))

    return FlowFieldArtwork(width=w, height=h, streamlines=streamlines)
