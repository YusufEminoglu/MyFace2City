# Changelog

All notable changes to **`myface2city`** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.10.0] - 2026-08-30

### Added
- **Artisan Marquetry Wood Inlay & Parquet Mosaic (`marquetry_wood_inlay_art.py`)**: Added `generate_marquetry_portrait` converting photos to fine exotic wood veneer parquet tessellations.
- **FLIR Thermal Infrared Heatmap Art (`thermal_infrared_palette_art.py`)**: Added `generate_thermal_infrared_portrait` mapping facial luminescence to false-color Ironbow spectral isotherms.

## [0.9.0] - 2026-08-30

### Added
- **Architectural Cyanotype Blueprint & Sunprint Art (`blueprint_cyanotype_art.py`)**: Added `generate_blueprint_portrait` producing Prussian blue engineering drafting grids and technical building elevations.
- **Synthwave & Cyberpunk Neon Glow Vectors (`neon_cyberpunk_vector.py`)**: Added `generate_cyberpunk_neon_portrait` with perspective horizon grid lines and glowing laser vector nodes.

## [0.8.0] - 2026-08-30

### Added
- **Topographic Linocut & Woodblock Relief Print Art (`topographic_linocut_art.py`)**: Added `generate_linocut_portrait` simulating Japanese Moku-Hanga wood-grain carve grooves and relief gouge ink textures.
- **Cathedral Stained Glass & Lead Came Mosaic (`stained_glass_cathedral.py`)**: Added `generate_stained_glass_portrait` creating luminous polygonal glass facets with dark lead came boundaries.

## [0.7.0] - 2026-08-30

### Added
- **2.5D Axonometric / Isometric Urban Voxel Cityscape Generator (`isometric_block_art.py`)**: Added `generate_isometric_city_portrait` turning image luminance into 3D skyscraper heights and isometric SVG geometry.
- **Generative Fluid Watercolor Cartography & Pigment Washes (`watercolor_cartography.py`)**: Added `apply_watercolor_wash_portrait` with turbulence displacement maps and edge-bleed pigment diffusion.

## [0.6.0] - 2026-08-30

### Added
- **Architectural & Copperplate Cross-Hatching Engraver (`line_hatching.py`)**: Added `generate_engraved_hatching_art` with multi-angle pen-and-ink stroke density modulation and SVG export.
- **Classical Error Diffusion & Bayer Ordered Matrix Dithering (`dithering_matrix.py`)**: Added `generate_ordered_dither_portrait` (Bayer 4x4) and `apply_error_diffusion_dither` (Floyd-Steinberg & Atkinson).

## [0.5.0] - 2026-08-30

### Added
- **Typographic & ASCII Portrait Art Generator (`ascii_art.py`)**: Added `generate_ascii_map_art` creating density-calibrated typographic portraits with HTML/plain-text exporters.
- **Reaction-Diffusion Turing Pattern Synthesizer (`reaction_diffusion.py`)**: Added `generate_turing_portrait` and `simulate_gray_scott` solving 2D discrete Laplacian reaction-diffusion PDEs.

## [0.4.0] - 2026-08-30

### Added
- **Flow-Field Vector Streamline Art (`flow_field.py`)**: Added `generate_flow_field_art` tracing organic streamlines guided by edge gradients and luminance.
- **CMYK Halftone Separation Plates (`color_separation.py`)**: Added `generate_cmyk_screen_layers` and SVG stencil exporter for screen printing and risograph.
- **Isometric 2.5D Voxel Art Generator (`voxel_art.py`)**: Added `generate_isometric_voxel_art` converting portrait luminance to 3D voxel block heights.
- **Bilateral Filtering & Contrast Enhancement (`tone_filter.py`)**: Added `bilateral_texture_filter` and `clahe_contrast_enhancer`.

## [0.2.0] - 2026-08-30

### Added
- **Centroidal Voronoi Tessellation (CVT) & Mosaic Art (`voronoi_art.py`)**:
  - `generate_voronoi_stipple`: Lloyd's relaxation algorithm weighted by local image density/contrast.
  - Generates organic Voronoi polygonal cell mosaic art with SVG and GeoJSON polygonal feature export.
- **Multi-Layer 3D Relief & Extrusion Mesh Exporter (`relief.py`)**:
  - `generate_3d_relief_mesh`: Fuses 2D portrait/map luminance and elevation heights into 3D geometric surfaces (`ReliefMesh3D`).
  - Direct export to standard 3D Wavefront `.OBJ` mesh files with vertices, normals, and UVs for 3D printing and 3D rendering.

## [0.1.0] - 2026-08-26

### Added
- Initial standalone release of `myface2city` (Python port of QGIS `02Urban Portrait`).
- **UrbanPortrait Engine**: Live luminance sampling, auto-contrast quantile stretching, gamma adjustment, and edge emphasis.
- **10 Curated Art Presets**: Ink Portrait, Neon Night, Blueprint, Sepia Blocks, Negative City, Cyberpunk 2077, Vintage Engraving, Thermal Heatmap, Emerald Eco-Map, and Nordic Slate.
- **Halftone & Vector Stippling Generator**: Variable-radius engraving dot grid calculation.
- **OpenStreetMap Overpass API Client**: Automated road and building footprint acquisition for arbitrary bounding boxes.
- **SVG Artwork & GeoJSON Exporters**: Standalone high-resolution SVG rendering and styled GeoJSON generation.
- **CLI Suite**: `myface2city render`, `myface2city stipple`, and `myface2city presets`.
- High-resolution SVG logo and interactive documentation site.
