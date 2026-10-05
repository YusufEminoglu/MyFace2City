# -*- coding: utf-8 -*-
"""Isometric 2.5D Pixel & Voxel Block City Art Generator for myface2city."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image


@dataclass
class VoxelBlock:
    """A single 3D isometric voxel building/pixel column."""

    grid_x: int
    grid_y: int
    height_voxels: int
    top_color_hex: str
    left_color_hex: str
    right_color_hex: str


@dataclass
class VoxelScene:
    """Complete isometric 2.5D cityscape/portrait scene."""

    grid_cols: int
    grid_rows: int
    block_width: float  # Base pixel width of isometric diamond
    blocks: list[VoxelBlock]

    def to_svg(self, background: str = "#1e1e2e") -> str:
        """Render isometric voxel blocks with realistic top, left, and right shade faces."""
        bw = self.block_width
        bh = bw * 0.5  # Isometric height ratio 1:2
        unit_h = bh * 0.8  # Height step per voxel

        # Calculate canvas size
        svg_w = int((self.grid_cols + self.grid_rows) * (bw / 2.0) + bw * 2)
        svg_h = int((self.grid_cols + self.grid_rows) * (bh / 2.0) + unit_h * 25 + bh * 4)

        origin_x = svg_w / 2.0
        origin_y = bh * 2.0

        polygons: list[str] = []

        # Sort blocks back-to-front (painter's algorithm)
        sorted_blocks = sorted(self.blocks, key=lambda b: (b.grid_x + b.grid_y))

        for b in sorted_blocks:
            # Isometric grid projection
            iso_x = origin_x + (b.grid_x - b.grid_y) * (bw / 2.0)
            iso_y = origin_y + (b.grid_x + b.grid_y) * (bh / 2.0)

            z_offset = b.height_voxels * unit_h
            top_y = iso_y - z_offset

            # Top Face (Diamond)
            top_pts = f"{iso_x:.1f},{top_y:.1f} {iso_x + bw/2:.1f},{top_y + bh/2:.1f} {iso_x:.1f},{top_y + bh:.1f} {iso_x - bw/2:.1f},{top_y + bh/2:.1f}"
            polygons.append(f'<polygon points="{top_pts}" fill="{b.top_color_hex}" stroke="#000000" stroke-width="0.3" />')

            # Left Face
            if z_offset > 0:
                left_pts = f"{iso_x - bw/2:.1f},{top_y + bh/2:.1f} {iso_x:.1f},{top_y + bh:.1f} {iso_x:.1f},{iso_y + bh:.1f} {iso_x - bw/2:.1f},{iso_y + bh/2:.1f}"
                polygons.append(f'<polygon points="{left_pts}" fill="{b.left_color_hex}" stroke="#000000" stroke-width="0.3" />')

                # Right Face
                right_pts = f"{iso_x:.1f},{top_y + bh:.1f} {iso_x + bw/2:.1f},{top_y + bh/2:.1f} {iso_x + bw/2:.1f},{iso_y + bh/2:.1f} {iso_x:.1f},{iso_y + bh:.1f}"
                polygons.append(f'<polygon points="{right_pts}" fill="{b.right_color_hex}" stroke="#000000" stroke-width="0.3" />')

        joined = "\n  ".join(polygons)
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}">
  <rect width="100%" height="100%" fill="{background}" />
  {joined}
</svg>"""

    def save_svg(self, output_path: str | Path) -> Path:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(self.to_svg(), encoding="utf-8")
        return out


def generate_isometric_voxel_art(
    image: Image.Image | str | Path,
    grid_resolution: int = 32,
    max_height_voxels: int = 16,
    block_width: float = 16.0,
) -> VoxelScene:
    """Convert portrait image luminance into a 2.5D isometric voxel block scene."""
    if not isinstance(image, Image.Image):
        img = Image.open(image).convert("RGB")
    else:
        img = image.convert("RGB")

    small = img.resize((grid_resolution, grid_resolution), Image.Resampling.LANCZOS)
    pixels = small.load()

    blocks: list[VoxelBlock] = []

    for r in range(grid_resolution):
        for c in range(grid_resolution):
            red, green, blue = pixels[c, r][:3]
            lum = (0.299 * red + 0.587 * green + 0.114 * blue) / 255.0

            # Height inversely or directly proportional to luminance
            height = int((1.0 - lum) * max_height_voxels) + 1

            # Top color
            top_hex = f"#{red:02x}{green:02x}{blue:02x}"
            # Left face is shadowed (~75%)
            lr, lg, lb = int(red * 0.75), int(green * 0.75), int(blue * 0.75)
            left_hex = f"#{lr:02x}{lg:02x}{lb:02x}"
            # Right face is darker shadow (~55%)
            rr, rg, rb = int(red * 0.55), int(green * 0.55), int(blue * 0.55)
            right_hex = f"#{rr:02x}{rg:02x}{rb:02x}"

            blocks.append(
                VoxelBlock(
                    grid_x=c,
                    grid_y=r,
                    height_voxels=height,
                    top_color_hex=top_hex,
                    left_color_hex=left_hex,
                    right_color_hex=right_hex,
                )
            )

    return VoxelScene(
        grid_cols=grid_resolution,
        grid_rows=grid_resolution,
        block_width=block_width,
        blocks=blocks,
    )
