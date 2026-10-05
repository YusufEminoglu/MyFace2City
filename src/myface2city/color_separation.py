# -*- coding: utf-8 -*-
"""Multi-Layer Color Separation & Screen-Printing Plates Generator for myface2city."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image


@dataclass
class ScreenPrintPlate:
    """A single color ink plate / channel separation."""

    plate_name: str  # 'Cyan', 'Magenta', 'Yellow', 'Black', 'Fluorescent Pink', etc.
    hex_ink_color: str
    halftone_angle_degrees: float
    dot_radius_matrix: list[list[float]]  # Normalized dot sizes (0.0 to 1.0)


@dataclass
class ColorSeparationArtwork:
    """Collection of separated color layers for physical risograph/screen printing."""

    width: int
    height: int
    plates: list[ScreenPrintPlate]

    def export_plates_svg(self, output_dir: str | Path, cell_size: int = 6) -> list[Path]:
        """Export each plate as a separate vector SVG stencil ready for plotter/laser/printing."""
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        saved_paths: list[Path] = []

        for plate in self.plates:
            svg_file = out_dir / f"plate_{plate.plate_name.lower().replace(' ', '_')}.svg"
            circles = []
            rows = len(plate.dot_radius_matrix)
            cols = len(plate.dot_radius_matrix[0]) if rows > 0 else 0

            max_r = (cell_size / 2.0) * 0.95
            for r in range(rows):
                for c in range(cols):
                    val = plate.dot_radius_matrix[r][c]
                    if val > 0.05:
                        cx = c * cell_size + cell_size / 2.0
                        cy = r * cell_size + cell_size / 2.0
                        rad = val * max_r
                        circles.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{rad:.2f}" fill="{plate.hex_ink_color}" />')

            joined = "\n  ".join(circles)
            w_px = cols * cell_size
            h_px = rows * cell_size
            svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w_px} {h_px}" width="{w_px}" height="{h_px}">
  <rect width="100%" height="100%" fill="#ffffff" />
  <!-- Plate: {plate.plate_name} | Angle: {plate.halftone_angle_degrees}° -->
  {joined}
</svg>"""
            svg_file.write_text(svg_content, encoding="utf-8")
            saved_paths.append(svg_file)

        return saved_paths


def generate_cmyk_screen_layers(
    image: Image.Image | str | Path,
    grid_cells_x: int = 50,
) -> ColorSeparationArtwork:
    """Decompose image into CMYK halftone screen printing plates."""
    if not isinstance(image, Image.Image):
        img = Image.open(image).convert("RGB")
    else:
        img = image.convert("RGB")

    w, h = img.size
    aspect = h / max(1, w)
    grid_cells_y = max(1, int(grid_cells_x * aspect))

    # Resize down to grid size
    small_img = img.resize((grid_cells_x, grid_cells_y), Image.Resampling.BOX)
    pixels = small_img.load()

    c_mat = [[0.0] * grid_cells_x for _ in range(grid_cells_y)]
    m_mat = [[0.0] * grid_cells_x for _ in range(grid_cells_y)]
    y_mat = [[0.0] * grid_cells_x for _ in range(grid_cells_y)]
    k_mat = [[0.0] * grid_cells_x for _ in range(grid_cells_y)]

    for r in range(grid_cells_y):
        for c in range(grid_cells_x):
            red, green, blue = pixels[c, r][:3]
            # Standard RGB to CMYK
            rf, gf, bf = red / 255.0, green / 255.0, blue / 255.0
            k = 1.0 - max(rf, gf, bf)
            if k < 1.0:
                cyan = (1.0 - rf - k) / (1.0 - k)
                magenta = (1.0 - gf - k) / (1.0 - k)
                yellow = (1.0 - bf - k) / (1.0 - k)
            else:
                cyan, magenta, yellow = 0.0, 0.0, 0.0

            c_mat[r][c] = round(max(0.0, min(1.0, cyan)), 3)
            m_mat[r][c] = round(max(0.0, min(1.0, magenta)), 3)
            y_mat[r][c] = round(max(0.0, min(1.0, yellow)), 3)
            k_mat[r][c] = round(max(0.0, min(1.0, k)), 3)

    plates = [
        ScreenPrintPlate("Cyan", "#00ffff", 15.0, c_mat),
        ScreenPrintPlate("Magenta", "#ff00ff", 75.0, m_mat),
        ScreenPrintPlate("Yellow", "#ffff00", 0.0, y_mat),
        ScreenPrintPlate("Black", "#000000", 45.0, k_mat),
    ]

    return ColorSeparationArtwork(width=w, height=h, plates=plates)
