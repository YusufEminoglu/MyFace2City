# -*- coding: utf-8 -*-
"""2.5D Axonometric / Isometric Urban Voxel Cityscape Portrait Generator for myface2city."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image


@dataclass
class IsometricVoxel:
    grid_c: int
    grid_r: int
    height_voxels: int
    iso_screen_x: float
    iso_screen_y: float
    top_color_hex: str
    left_color_hex: str
    right_color_hex: str


@dataclass
class IsometricCityArtwork:
    """Axonometric 2.5D urban skyscraper voxel portrait."""

    width: int
    height: int
    voxels: list[IsometricVoxel]

    def to_svg(self, background_color: str = "#0f172a") -> str:
        # Sort voxels from back to front: (grid_r + grid_c)
        sorted_vox = sorted(self.voxels, key=lambda v: (v.grid_r + v.grid_c))

        cube_w = 16.0
        cube_h = 8.0  # standard 2:1 isometric ratio

        polys = []
        for v in sorted_vox:
            if v.height_voxels <= 0:
                continue

            cx = v.iso_screen_x
            cy = v.iso_screen_y
            vh = v.height_voxels * 4.0

            # Base points & Top points
            # Top rhombus
            t_top = (cx, cy - vh - cube_h)
            t_right = (cx + cube_w / 2.0, cy - vh)
            t_bot = (cx, cy - vh + cube_h)
            t_left = (cx - cube_w / 2.0, cy - vh)

            top_pts = f"{t_top[0]:.1f},{t_top[1]:.1f} {t_right[0]:.1f},{t_right[1]:.1f} {t_bot[0]:.1f},{t_bot[1]:.1f} {t_left[0]:.1f},{t_left[1]:.1f}"

            # Left face
            l_pts = f"{t_left[0]:.1f},{t_left[1]:.1f} {t_bot[0]:.1f},{t_bot[1]:.1f} {t_bot[0]:.1f},{t_bot[1] + vh:.1f} {t_left[0]:.1f},{t_left[1] + vh:.1f}"

            # Right face
            r_pts = f"{t_bot[0]:.1f},{t_bot[1]:.1f} {t_right[0]:.1f},{t_right[1]:.1f} {t_right[0]:.1f},{t_right[1] + vh:.1f} {t_bot[0]:.1f},{t_bot[1] + vh:.1f}"

            polys.append(f'<polygon points="{l_pts}" fill="{v.left_color_hex}" stroke="#000000" stroke-width="0.5" />')
            polys.append(f'<polygon points="{r_pts}" fill="{v.right_color_hex}" stroke="#000000" stroke-width="0.5" />')
            polys.append(f'<polygon points="{top_pts}" fill="{v.top_color_hex}" stroke="#000000" stroke-width="0.5" />')

        joined = "\n  ".join(polys)
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" width="{self.width}" height="{self.height}">
  <rect width="100%" height="100%" fill="{background_color}" />
  {joined}
</svg>"""

    def save_svg(self, output_path: str | Path) -> Path:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(self.to_svg(), encoding="utf-8")
        return out


def generate_isometric_city_portrait(
    image: Image.Image | str | Path,
    grid_size: int = 16,
    max_building_height_voxels: int = 12,
    palette_top: str = "#38bdf8",
    palette_left: str = "#0284c7",
    palette_right: str = "#0369a1",
) -> IsometricCityArtwork:
    """Convert portrait image tone into 2.5D extruded skyscraper voxel blocks."""
    if not isinstance(image, Image.Image):
        img = Image.open(image).convert("L")
    else:
        img = image.convert("L")

    img_scaled = img.resize((grid_size, grid_size), Image.Resampling.BILINEAR)
    pixels = img_scaled.load()

    cube_w = 24.0
    cube_h = 12.0
    canvas_w = int((grid_size * 2 + 4) * cube_w / 2.0)
    canvas_h = int((grid_size * 2 + max_building_height_voxels + 4) * cube_h)
    origin_x = canvas_w / 2.0
    origin_y = canvas_h * 0.45

    voxels: list[IsometricVoxel] = []

    for r in range(grid_size):
        for c in range(grid_size):
            val = 1.0 - (pixels[c, r] / 255.0)  # darker = taller building
            h_vox = int(val * max_building_height_voxels)

            # Isometric projection screen coordinates
            sx = origin_x + (c - r) * (cube_w / 2.0)
            sy = origin_y + (c + r) * (cube_h / 2.0)

            voxels.append(
                IsometricVoxel(
                    grid_c=c,
                    grid_r=r,
                    height_voxels=h_vox,
                    iso_screen_x=sx,
                    iso_screen_y=sy,
                    top_color_hex=palette_top,
                    left_color_hex=palette_left,
                    right_color_hex=palette_right,
                )
            )

    return IsometricCityArtwork(width=canvas_w, height=canvas_h, voxels=voxels)
