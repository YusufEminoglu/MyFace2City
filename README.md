# MyFace2City — Optical Urban Portrait & Generative Cartography Engine

<p align="center">
  <img src="https://geophilo.com/assets/sdk_icons/myface2city.svg" alt="MyFace2City Logo" width="680">
</p>

<p align="center">
  <a href="https://pypi.org/project/myface2city/"><img src="https://img.shields.io/pypi/v/myface2city?color=FF0055&label=PyPI%20Version" alt="PyPI"></a>
  <a href="https://pypi.org/project/myface2city/"><img src="https://img.shields.io/pypi/dm/myface2city?color=7000FF&label=Downloads" alt="PyPI Downloads"></a>
  <a href="https://geophilo.com/"><img src="https://img.shields.io/badge/docs-GEOPHILO-10b981.svg" alt="Documentation"></a>
  <a href="https://gitlab.com/geospacephilo/MyFace2City/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-emerald.svg" alt="License: MIT"></a>
  <a href="https://gitlab.com/geospacephilo/MyFace2City/actions"><img src="https://img.shields.io/badge/CI-Passing-brightgreen.svg" alt="CI"></a>
</p>

---

## 🌐 Live Interactive Studio & Documentation

Explore the **in-browser Generative Cartography Studio** and comprehensive technical reference manual:

👉 **[https://geophilo.com/](https://geophilo.com/)**

Upload any portrait photo, choose from 10 curated artistic presets, and export scalable SVG posters directly in your browser.

---

## 📖 Overview

**`MyFace2City`** is a pure-Python generative cartography and optical portrait engine. It turns road networks, building footprints, land-use boundaries, and vector parcels into live optical portraits.

By binding a raster face/portrait photo to a geographic frame, each vector feature samples underlying image luminance and receives a reversible, rule-based cartographic style—without mutating source geometries or attributes.

---

## ✨ Features

- 🎭 **UrbanPortrait Engine:** Live luminance sampling with distortion-free aspect-ratio fitting.
- 🎨 **10 Curated Art Presets:** Ink Portrait, Neon Night, Blueprint, Sepia Blocks, Negative City, Cyberpunk 2077, Vintage Engraving, Thermal Heatmap, Emerald Eco-Map, and Nordic Slate.
- 🔘 **Algorithmic Halftone & Vector Stippling:** Generates variable-radius engraving dot grids across geographic regions.
- 🗺️ **OpenStreetMap Acquisition (Overpass API):** Built-in client to fetch roads and buildings for any bounding box.
- 🖼️ **Standalone Scalable Vector SVG Exporter:** Generates high-resolution SVG posters with dark/light themes and glowing underlays.
- ⚙️ **Smart Image Enhancement:** Automatic histogram quantile contrast stretching, gamma correction, inversion, and edge emphasis.
- 💻 **CLI Interface:** Fast command-line rendering (`myface2city render`, `myface2city stipple`, `myface2city presets`).

---

## 🚀 Quick Start

### Installation

```bash
pip install myface2city
```

### Python API

```python
import myface2city as mfc

# 1. Initialize portrait engine with image and geographic bounds
bounds = (27.10, 38.40, 27.20, 38.50)  # (min_lon, min_lat, max_lon, max_lat)
portrait = mfc.UrbanPortrait("face.jpg", bounds)

# 2. Fetch OSM vector roads & buildings or load local GeoJSON
geojson_data = mfc.fetch_osm_network(bounds)

# 3. Apply optical portrait styling with Cyberpunk preset
styled_geojson = portrait.process_geojson(geojson_data, palette="Cyberpunk 2077")

# 4. Export high-resolution standalone vector SVG poster
mfc.export_svg(styled_geojson, "urban_portrait.svg", preset="Cyberpunk 2077")
```

### Halftone Vector Stippling

```python
import myface2city as mfc
from PIL import Image

img = Image.open("face.jpg").convert("L")
w, h = img.size
pixels = img.load()

# Define sampling callback
def sample_fn(u: float, v: float) -> float:
    px = int(max(0.0, min(1.0, u)) * (w - 1))
    py = int(max(0.0, min(1.0, v)) * (h - 1))
    return float(pixels[px, py])

# Generate 80x80 halftone stipple dot grid
points = mfc.calculate_stipple_points(
    0.0, 0.0, 100.0, 100.0,
    grid_cols=80, grid_rows=80,
    sample_fn=sample_fn,
    max_radius=4.0,
    preset="Ink Portrait"
)

stipple_geojson = mfc.stipple_to_geojson(points)
mfc.export_svg(stipple_geojson, "stipple_art.svg", preset="Ink Portrait")
```

---

## 💻 CLI Usage

```bash
# List all 10 art presets
myface2city presets

# Render face onto OpenStreetMap network
myface2city render --image face.jpg --osm-bbox 27.10,38.40,27.20,38.50 --preset "Cyberpunk 2077" --output portrait.svg

# Generate halftone stippling engraving
myface2city stipple --image face.jpg --cols 90 --rows 90 --preset "Vintage Engraving" --output engraving.svg
```

---

## 📜 License

MIT License © 2026 [Yusuf Eminoğlu](https://github.com/YusufEminoglu).
