# -*- coding: utf-8 -*-
"""
MyFace2City — Turn urban street networks, building footprints, and vector maps into live optical portrait art.
"""

from __future__ import annotations

__version__ = "0.1.0"
__author__ = "Yusuf Eminoğlu"

from . import cli
from .engine import RenderConfig, UrbanPortrait
from .export import export_svg, render_svg_artwork
from .osm import fetch_osm_network, generate_synthetic_urban_grid
from .presets import (
    PRESETS,
    Palette,
    get_preset,
    list_presets,
    load_custom_palette,
    save_custom_palette,
)
from .profile import (
    NormalizedPoint,
    adjust_luminance,
    blend_edge,
    fit_bounds_to_aspect,
    map_to_normalized,
    quantile_limits,
)
from .stipple import calculate_stipple_points, stipple_to_geojson

__all__ = [
    "__version__",
    "cli",
    # Core Engine
    "UrbanPortrait",
    "RenderConfig",
    # Presets & Palettes
    "PRESETS",
    "Palette",
    "get_preset",
    "list_presets",
    "load_custom_palette",
    "save_custom_palette",
    # Algorithmic Halftone & Stippling
    "calculate_stipple_points",
    "stipple_to_geojson",
    # Exporter
    "render_svg_artwork",
    "export_svg",
    # OpenStreetMap
    "fetch_osm_network",
    "generate_synthetic_urban_grid",
    # Profile & Tone Math
    "NormalizedPoint",
    "fit_bounds_to_aspect",
    "map_to_normalized",
    "adjust_luminance",
    "quantile_limits",
    "blend_edge",
]
