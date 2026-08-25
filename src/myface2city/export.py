"""
Artwork Exporter: Standalone Scalable Vector Graphics (SVG) Posters & QGIS QML Styles.
"""

from __future__ import annotations

import html
import math
from pathlib import Path
from typing import Any

from .presets import Palette, get_preset


def render_svg_artwork(
    geojson_data: dict[str, Any],
    bounds: tuple[float, float, float, float] | None = None,
    preset: str | Palette = "Ink Portrait",
    svg_width: int = 1200,
    svg_height: int = 1200,
    margin: int = 40,
) -> str:
    """Render styled vector GeoJSON features into a standalone high-resolution SVG artwork poster."""
    palette = get_preset(preset) if isinstance(preset, str) else preset
    features = geojson_data.get("features", [])

    # Calculate bounding box from data if not provided
    if bounds is None:
        min_x, min_y, max_x, max_y = float("inf"), float("inf"), float("-inf"), float("-inf")
        for feat in features:
            geom = feat.get("geometry", {})
            coords = geom.get("coordinates", [])
            _update_bbox(coords, min_x, min_y, max_x, max_y)
        if math.isinf(min_x):
            bounds = (0.0, 0.0, 1.0, 1.0)
        else:
            bounds = (min_x, min_y, max_x, max_y)

    min_x, min_y, max_x, max_y = bounds
    geo_w = max(1e-9, max_x - min_x)
    geo_h = max(1e-9, max_y - min_y)

    draw_w = svg_width - 2 * margin
    draw_h = svg_height - 2 * margin

    def world_to_screen(x: float, y: float) -> tuple[float, float]:
        sx = margin + ((x - min_x) / geo_w) * draw_w
        sy = margin + ((max_y - y) / geo_h) * draw_h  # SVG Y down
        return round(sx, 2), round(sy, 2)

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">',
        f'  <rect width="{svg_width}" height="{svg_height}" fill="{palette.background}" />',
        '  <g id="urban-portrait-elements">',
    ]

    for feat in features:
        props = feat.get("properties", {})
        if props.get("_is_hidden", False):
            continue

        color = props.get("_portrait_color") or props.get("color") or palette.colors[0]
        stroke_w = props.get("_stroke_width") or props.get("radius") or 1.0
        opacity = props.get("_opacity", 1.0)

        geom = feat.get("geometry", {})
        g_type = geom.get("type", "")
        coords = geom.get("coordinates", [])

        if g_type == "Point" and len(coords) >= 2:
            sx, sy = world_to_screen(coords[0], coords[1])
            radius = stroke_w
            svg_parts.append(f'    <circle cx="{sx}" cy="{sy}" r="{radius}" fill="{color}" opacity="{opacity}" />')

        elif g_type == "LineString" and len(coords) >= 2:
            pts = [world_to_screen(p[0], p[1]) for p in coords]
            d_str = f"M {pts[0][0]} {pts[0][1]} " + " ".join(f"L {p[0]} {p[1]}" for p in pts[1:])
            svg_parts.append(
                f'    <path d="{d_str}" fill="none" stroke="{color}" stroke-width="{stroke_w}" stroke-linecap="round" stroke-linejoin="round" opacity="{opacity}" />'
            )

        elif g_type == "Polygon" and coords:
            for ring in coords:
                if len(ring) >= 3:
                    pts = [world_to_screen(p[0], p[1]) for p in ring]
                    d_str = f"M {pts[0][0]} {pts[0][1]} " + " ".join(f"L {p[0]} {p[1]}" for p in pts[1:]) + " Z"
                    svg_parts.append(
                        f'    <path d="{d_str}" fill="{color}" fill-opacity="{opacity * 0.4}" stroke="{color}" stroke-width="{stroke_w * 0.7}" stroke-linejoin="round" />'
                    )

    svg_parts.append("  </g>")
    # Subtle signature footer
    svg_parts.append(
        f'  <text x="{margin}" y="{svg_height - margin + 20}" font-family="sans-serif" font-size="11" fill="{palette.colors[2]}" opacity="0.6">Rendered with MyFace2City &#183; Preset: {html.escape(palette.name)}</text>'
    )
    svg_parts.append("</svg>")

    return "\n".join(svg_parts)


def export_svg(
    geojson_data: dict[str, Any],
    output_path: str | Path,
    preset: str | Palette = "Ink Portrait",
    width: int = 1200,
    height: int = 1200,
) -> Path:
    """Render and save SVG artwork to disk."""
    svg_str = render_svg_artwork(geojson_data, preset=preset, svg_width=width, svg_height=height)
    p = Path(output_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(svg_str, encoding="utf-8")
    return p


def _update_bbox(coords: Any, min_x: float, min_y: float, max_x: float, max_y: float) -> None:
    if not coords:
        return
    if isinstance(coords[0], (int, float)):
        min_x = min(min_x, coords[0])
        max_x = max(max_x, coords[0])
        min_y = min(min_y, coords[1])
        max_y = max(max_y, coords[1])
    else:
        for sub in coords:
            _update_bbox(sub, min_x, min_y, max_x, max_y)
