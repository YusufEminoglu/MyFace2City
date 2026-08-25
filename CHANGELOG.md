# Changelog

All notable changes to **`myface2city`** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
