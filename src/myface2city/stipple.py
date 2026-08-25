# -*- coding: utf-8 -*-
"""
Algorithmic Halftone and Vector Stippling Engraving Generator for MyFace2City.
"""

from __future__ import annotations

import math
from typing import Any, Callable

from .presets import Palette, get_preset


def calculate_stipple_points(
    min_x: float,
    min_y: float,
    max_x: float,
    max_y: float,
    grid_cols: int,
    grid_rows: int,
    sample_fn: Callable[[float, float], float],
    max_radius: float = 5.0,
    gamma: float = 1.0,
    invert: bool = False,
    preset: str | Palette = "Ink Portrait",
) -> list[dict[str, Any]]:
    """Generate variable-radius halftone stipple dots from an image sampling function."""
    values = (min_x, min_y, max_x, max_y, max_radius, gamma)
    if any(not math.isfinite(float(val)) for val in values):
        raise ValueError("Stipple bounds and rendering values must be finite numbers.")
    if max_x <= min_x or max_y <= min_y:
        raise ValueError("Stipple bounds must have a positive width and height.")
    if int(grid_cols) < 2 or int(grid_rows) < 2:
        raise ValueError("Stipple grids require at least 2 rows and 2 columns.")
    if max_radius <= 0.0 or gamma <= 0.0:
        raise ValueError("Stipple max radius and gamma must be positive.")

    palette = get_preset(preset) if isinstance(preset, str) else preset
    dx = (max_x - min_x) / max(1, grid_cols - 1)
    dy = (max_y - min_y) / max(1, grid_rows - 1)
    points: list[dict[str, Any]] = []

    for row in range(grid_rows):
        v = row / max(1, grid_rows - 1)
        y = max_y - row * dy  # Top to bottom
        for col in range(grid_cols):
            u = col / max(1, grid_cols - 1)
            x = min_x + col * dx

            luma = sample_fn(u, v)
            if invert:
                luma = 255.0 - luma
            luma = max(0, min(255, int(round(luma))))

            # Darker pixels produce larger dots in halftone engraving
            intensity = 1.0 - (luma / 255.0)
            if gamma != 1.0 and intensity > 0.0:
                intensity = math.pow(intensity, gamma)

            radius = max_radius * intensity
            if radius < 0.05:
                continue

            tone_bin = min(4, int(luma / 52))
            color = palette.colors[tone_bin]

            points.append(
                {
                    "id": len(points) + 1,
                    "x": round(x, 6),
                    "y": round(y, 6),
                    "u": round(u, 4),
                    "v": round(v, 4),
                    "luminance": luma,
                    "radius": round(radius, 3),
                    "tone_bin": tone_bin,
                    "color": color,
                }
            )

    return points


def stipple_to_geojson(
    points: list[dict[str, Any]],
) -> dict[str, Any]:
    """Convert calculated stipple points to a standard GeoJSON FeatureCollection."""
    features = []
    for pt in points:
        features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [pt["x"], pt["y"]],
                },
                "properties": {
                    "id": pt["id"],
                    "luminance": pt["luminance"],
                    "radius": pt["radius"],
                    "tone_bin": pt["tone_bin"],
                    "color": pt["color"],
                },
            }
        )
    return {"type": "FeatureCollection", "features": features}
