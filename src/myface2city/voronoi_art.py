# -*- coding: utf-8 -*-
"""Centroidal Voronoi Tessellation (CVT) & Organic Delaunay Mosaic Art Generator for MyFace2City."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

from PIL import Image

from .presets import Palette, get_preset


@dataclass
class VoronoiCell:
    """Represents a single Voronoi cell with centroid, boundary polygon, and tone."""

    centroid: tuple[float, float]
    polygon: list[tuple[float, float]]
    luminance: float  # 0.0 (dark) to 1.0 (light)
    color_hex: str = "#000000"


@dataclass
class VoronoiArtwork:
    """Complete Voronoi mosaic artwork data."""

    width: int
    height: int
    cells: list[VoronoiCell]
    palette: Palette

    def to_svg(self) -> str:
        """Export Voronoi artwork as scalable SVG."""
        svg_lines = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" width="{self.width}" height="{self.height}">',
            f'  <rect width="100%" height="100%" fill="{self.palette.background}" />',
            '  <g id="voronoi-cells">',
        ]

        for cell in self.cells:
            if len(cell.polygon) < 3:
                continue
            pts_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in cell.polygon)
            svg_lines.append(
                f'    <polygon points="{pts_str}" fill="{cell.color_hex}" stroke="{self.palette.background}" stroke-width="0.75" />'
            )

        svg_lines.append("  </g>")
        svg_lines.append("</svg>")
        return "\n".join(svg_lines)

    def to_geojson(self) -> dict[str, Any]:
        """Convert Voronoi cells to GeoJSON Polygon features."""
        features = []
        for i, cell in enumerate(self.cells):
            if len(cell.polygon) < 3:
                continue
            coords = [[x, y] for x, y in cell.polygon]
            if coords[0] != coords[-1]:
                coords.append(coords[0])
            features.append(
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [coords],
                    },
                    "properties": {
                        "cell_id": i,
                        "centroid_x": round(cell.centroid[0], 2),
                        "centroid_y": round(cell.centroid[1], 2),
                        "luminance": round(cell.luminance, 3),
                        "fill_color": cell.color_hex,
                    },
                }
            )
        return {"type": "FeatureCollection", "features": features}


def generate_voronoi_stipple(
    image: Image.Image,
    preset: str | Palette = "Ink Portrait",
    target_points: int = 400,
    iterations: int = 5,
) -> VoronoiArtwork:
    """Generate Centroidal Voronoi Tessellation (CVT) optical mosaic from an input image.

    Args:
        image: PIL Image object.
        preset: Name of color preset or Palette object.
        target_points: Number of initial Voronoi seed points.
        iterations: Number of Lloyd's relaxation steps.

    Returns:
        VoronoiArtwork containing the relaxed cells and colors.
    """
    pal = get_preset(preset) if isinstance(preset, str) else preset
    gray = image.convert("L")
    w, h = gray.size
    pixels = gray.load()

    # Step 1: Initialize random or density-weighted points
    import random
    rng = random.Random(42)

    # Sample points inversely proportional to brightness (darker = denser)
    points: list[list[float]] = []
    attempts = 0
    max_attempts = target_points * 50

    while len(points) < target_points and attempts < max_attempts:
        attempts += 1
        rx = rng.uniform(0, w - 1)
        ry = rng.uniform(0, h - 1)
        lum = pixels[int(rx), int(ry)] / 255.0  # 0.0 dark to 1.0 bright
        accept_prob = (1.0 - lum) ** 1.5 + 0.05
        if rng.random() < accept_prob:
            points.append([rx, ry])

    if not points:
        # Fallback grid
        step_x = max(1, w // int(math.sqrt(target_points)))
        step_y = max(1, h // int(math.sqrt(target_points)))
        for x in range(step_x // 2, w, step_x):
            for y in range(step_y // 2, h, step_y):
                points.append([float(x), float(y)])

    # Step 2: Lloyd's relaxation approximation using discrete grid assignment
    # Create low-res sampling grid for relaxation
    grid_res = 60
    gw = grid_res
    gh = int(grid_res * (h / w))
    gh = max(10, gh)

    for _ in range(iterations):
        accum_x = [0.0] * len(points)
        accum_y = [0.0] * len(points)
        accum_w = [0.0] * len(points)

        for gx in range(gw):
            px = (gx + 0.5) * (w / gw)
            for gy in range(gh):
                py = (gy + 0.5) * (h / gh)
                lum = pixels[min(w - 1, int(px)), min(h - 1, int(py))] / 255.0
                weight = (1.0 - lum) + 0.05

                # Find nearest seed
                best_idx = 0
                best_dist_sq = float("inf")
                for p_idx, pt in enumerate(points):
                    d2 = (pt[0] - px) ** 2 + (pt[1] - py) ** 2
                    if d2 < best_dist_sq:
                        best_dist_sq = d2
                        best_idx = p_idx

                accum_x[best_idx] += px * weight
                accum_y[best_idx] += py * weight
                accum_w[best_idx] += weight

        # Update points to weighted centroids
        for i in range(len(points)):
            if accum_w[i] > 0:
                points[i][0] = accum_x[i] / accum_w[i]
                points[i][1] = accum_y[i] / accum_w[i]

    # Step 3: Construct bounding polygon cells around each seed point
    cells: list[VoronoiCell] = []
    # Build approximate convex polygonal cells for each seed
    for idx, (px, py) in enumerate(points):
        lum = pixels[min(w - 1, max(0, int(px))), min(h - 1, max(0, int(py)))] / 255.0
        # Color from palette
        c_idx = min(len(pal.colors) - 1, int(lum * len(pal.colors)))
        col = pal.colors[c_idx]

        # Generate geometric polygon for cell (octagon/hexagon radius based on distance to nearest neighbor)
        # Find distance to closest 3 neighbors
        dists = []
        for other_idx, other_pt in enumerate(points):
            if other_idx == idx:
                continue
            d = math.hypot(other_pt[0] - px, other_pt[1] - py)
            dists.append(d)
        dists.sort()
        r = (dists[0] if dists else 10.0) * 0.65

        # Create n-sided polygon ring
        num_sides = 6
        poly_ring = []
        for s in range(num_sides):
            ang = s * (2.0 * math.pi / num_sides)
            vx = max(0.0, min(float(w), px + r * math.cos(ang)))
            vy = max(0.0, min(float(h), py + r * math.sin(ang)))
            poly_ring.append((vx, vy))

        cells.append(
            VoronoiCell(
                centroid=(px, py),
                polygon=poly_ring,
                luminance=lum,
                color_hex=col,
            )
        )

    return VoronoiArtwork(
        width=w,
        height=h,
        cells=cells,
        palette=pal,
    )
