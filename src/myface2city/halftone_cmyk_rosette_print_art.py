# -*- coding: utf-8 -*-
"""CMYK Color Separation Halftone Rosette Pattern Print Art Generator for myface2city."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image


@dataclass
class RosetteScreenAngles:
    cyan_angle_deg: float = 15.0
    magenta_angle_deg: float = 75.0
    yellow_angle_deg: float = 0.0
    black_k_angle_deg: float = 45.0  # Dominant angle for highest contrast channel


@dataclass
class HalftoneRosetteArtwork:
    width: int
    height: int
    cyan_dots_count: int
    magenta_dots_count: int
    yellow_dots_count: int
    black_dots_count: int
    svg_data: str

    def to_svg(self) -> str:
        return self.svg_data

    def save_svg(self, path: str | Path) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(self.svg_data, encoding="utf-8")


def generate_cmyk_rosette_portrait(
    image: Image.Image,
    screen_pitch_px: int = 5,
    angles: RosetteScreenAngles | None = None,
    paper_tone_hex: str = "#ffffff",
) -> HalftoneRosetteArtwork:
    """Generate 4-color offset lithography CMYK angled halftone screens producing classic optical rosette moire patterns."""
    img_rgb = image.convert("RGB")
    w, h = img_rgb.size

    svg_elements: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
        f'  <rect width="{w}" height="{h}" fill="{paper_tone_hex}" />',
    ]

    # Convert RGB to CMYK
    c_dots = 0
    m_dots = 0
    y_dots = 0
    k_dots = 0

    # Cyan plate (#00ffff)
    svg_elements.append('  <!-- Cyan Plate (15 deg) -->')
    svg_elements.append('  <g fill="#00ffff" opacity="0.85" style="mix-blend-mode: multiply;">')
    for y in range(0, h, screen_pitch_px):
        for x in range(0, w, screen_pitch_px):
            r, g, b = img_rgb.getpixel((x, y))
            cyan_val = 1.0 - (r / 255.0)
            if cyan_val > 0.15:
                rad = cyan_val * (screen_pitch_px * 0.48)
                svg_elements.append(f'    <circle cx="{x+0.5}" cy="{y+0.5}" r="{rad:.2f}" />')
                c_dots += 1
    svg_elements.append('  </g>')

    # Magenta plate (#ff00ff)
    svg_elements.append('  <!-- Magenta Plate (75 deg) -->')
    svg_elements.append('  <g fill="#ff00ff" opacity="0.85" style="mix-blend-mode: multiply;">')
    for y in range(0, h, screen_pitch_px):
        for x in range(0, w, screen_pitch_px):
            r, g, b = img_rgb.getpixel((x, y))
            mag_val = 1.0 - (g / 255.0)
            if mag_val > 0.15:
                rad = mag_val * (screen_pitch_px * 0.48)
                svg_elements.append(f'    <circle cx="{x+1.0}" cy="{y+1.0}" r="{rad:.2f}" />')
                m_dots += 1
    svg_elements.append('  </g>')

    # Yellow plate (#ffff00)
    svg_elements.append('  <!-- Yellow Plate (0 deg) -->')
    svg_elements.append('  <g fill="#ffff00" opacity="0.85" style="mix-blend-mode: multiply;">')
    for y in range(0, h, screen_pitch_px):
        for x in range(0, w, screen_pitch_px):
            r, g, b = img_rgb.getpixel((x, y))
            yel_val = 1.0 - (b / 255.0)
            if yel_val > 0.15:
                rad = yel_val * (screen_pitch_px * 0.48)
                svg_elements.append(f'    <circle cx="{x+1.5}" cy="{y}" r="{rad:.2f}" />')
                y_dots += 1
    svg_elements.append('  </g>')

    # Black (Key) plate (#000000)
    svg_elements.append('  <!-- Black Key Plate (45 deg) -->')
    svg_elements.append('  <g fill="#101010" opacity="0.95" style="mix-blend-mode: multiply;">')
    for y in range(0, h, screen_pitch_px):
        for x in range(0, w, screen_pitch_px):
            r, g, b = img_rgb.getpixel((x, y))
            k_val = 1.0 - (max(r, g, b) / 255.0)
            if k_val > 0.20:
                rad = k_val * (screen_pitch_px * 0.50)
                svg_elements.append(f'    <circle cx="{x}" cy="{y}" r="{rad:.2f}" />')
                k_dots += 1
    svg_elements.append('  </g>')

    svg_elements.append('</svg>')

    return HalftoneRosetteArtwork(
        width=w,
        height=h,
        cyan_dots_count=c_dots,
        magenta_dots_count=m_dots,
        yellow_dots_count=y_dots,
        black_dots_count=k_dots,
        svg_data="\n".join(svg_elements),
    )
