"""
MyFace2City — Turn urban street networks, building footprints, and vector maps into live optical portrait art.
"""

from __future__ import annotations

__version__ = "0.9.0"
__author__ = "Yusuf Eminoğlu"

from . import cli
from .ascii_art import (
    ASCIIArtwork,
    generate_ascii_map_art,
)
from .blueprint_cyanotype_art import (
    BlueprintGridParams,
    CyanotypeArtwork,
    generate_blueprint_portrait,
)
from .color_separation import (
    ColorSeparationArtwork,
    ScreenPrintPlate,
    generate_cmyk_screen_layers,
)
from .dithering_matrix import (
    DitherArtwork,
    apply_error_diffusion_dither,
    generate_ordered_dither_portrait,
)
from .engine import RenderConfig, UrbanPortrait
from .export import export_svg, render_svg_artwork
from .flow_field import (
    FlowFieldArtwork,
    Streamline,
    generate_flow_field_art,
)
from .isometric_block_art import (
    IsometricCityArtwork,
    IsometricVoxel,
    generate_isometric_city_portrait,
)
from .line_hatching import (
    HatchingArtwork,
    HatchingStroke,
    generate_engraved_hatching_art,
)
from .neon_cyberpunk_vector import (
    CyberpunkArtwork,
    NeonPalette,
    generate_cyberpunk_neon_portrait,
)
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
from .reaction_diffusion import (
    TuringPatternArtwork,
    generate_turing_portrait,
    simulate_gray_scott,
)
from .relief import ReliefMesh3D, generate_3d_relief_mesh
from .stained_glass_cathedral import (
    GlassFacet,
    StainedGlassArtwork,
    generate_stained_glass_portrait,
)
from .stipple import calculate_stipple_points, stipple_to_geojson
from .tone_filter import (
    bilateral_texture_filter,
    clahe_contrast_enhancer,
)
from .topographic_linocut_art import (
    LinocutArtwork,
    LinocutCarveParams,
    generate_linocut_portrait,
)
from .voronoi_art import (
    VoronoiArtwork,
    VoronoiCell,
    generate_voronoi_stipple,
)
from .voxel_art import (
    VoxelBlock,
    VoxelScene,
    generate_isometric_voxel_art,
)
from .watercolor_cartography import (
    WatercolorArtwork,
    WatercolorPigmentParams,
    apply_watercolor_wash_portrait,
)

__all__ = [
    "__version__",
    "UrbanPortrait",
    "RenderConfig",
    # Voronoi & Delaunay Art
    "generate_voronoi_stipple",
    "VoronoiArtwork",
    "VoronoiCell",
    # 3D Relief Mesh
    "generate_3d_relief_mesh",
    "ReliefMesh3D",
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
    # Flow Field
    "generate_flow_field_art",
    "FlowFieldArtwork",
    "Streamline",
    # Color Separation
    "generate_cmyk_screen_layers",
    "ColorSeparationArtwork",
    "ScreenPrintPlate",
    # Voxel Art
    "generate_isometric_voxel_art",
    "VoxelScene",
    "VoxelBlock",
    # Tone Filter
    "bilateral_texture_filter",
    "clahe_contrast_enhancer",
    # Typographic & ASCII Art
    "generate_ascii_map_art",
    "ASCIIArtwork",
    # Reaction-Diffusion Turing Patterns
    "generate_turing_portrait",
    "TuringPatternArtwork",
    "simulate_gray_scott",
    # Architectural Cross-Hatching
    "generate_engraved_hatching_art",
    "HatchingArtwork",
    "HatchingStroke",
    # Ordered & Error Diffusion Dithering
    "generate_ordered_dither_portrait",
    "apply_error_diffusion_dither",
    "DitherArtwork",
    # 2.5D Isometric Cityscape
    "generate_isometric_city_portrait",
    "IsometricCityArtwork",
    "IsometricVoxel",
    # Watercolor Cartography
    "apply_watercolor_wash_portrait",
    "WatercolorArtwork",
    "WatercolorPigmentParams",
    # Topographic Linocut & Woodblock Art
    "generate_linocut_portrait",
    "LinocutArtwork",
    "LinocutCarveParams",
    # Cathedral Stained Glass Mosaic
    "generate_stained_glass_portrait",
    "StainedGlassArtwork",
    "GlassFacet",
    # Architectural Cyanotype Blueprint
    "generate_blueprint_portrait",
    "CyanotypeArtwork",
    "BlueprintGridParams",
    # Synthwave & Cyberpunk Neon Vectors
    "generate_cyberpunk_neon_portrait",
    "CyberpunkArtwork",
    "NeonPalette",
]
