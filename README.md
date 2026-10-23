# MyFace2City — Optical Urban Portrait & Generative Cartography Engine

<p align="center">
  <img src="https://geophilo.com/assets/sdk_icons/myface2city.svg" alt="MyFace2City Logo" width="680">
</p>

<p align="center">
  <a href="https://pypi.org/project/myface2city/"><img src="https://img.shields.io/pypi/v/myface2city?color=FF0055&label=PyPI%20Version" alt="PyPI"></a>
  <a href="https://pypi.org/project/myface2city/"><img src="https://img.shields.io/pypi/dm/myface2city?color=7000FF&label=Downloads" alt="PyPI Downloads"></a>
  <a href="https://geophilo.com/myface2city/"><img src="https://img.shields.io/badge/docs-GEOPHILO-10b981.svg" alt="Documentation"></a>
  <a href="https://gitlab.com/geospacephilo/MyFace2City/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-emerald.svg" alt="License: MIT"></a>
  <a href="https://gitlab.com/geospacephilo/MyFace2City/actions"><img src="https://img.shields.io/badge/CI-Passing-brightgreen.svg" alt="CI"></a>
</p>

---

## 🌐 Live Interactive Studio & Documentation

Explore the **in-browser Generative Cartography Studio** and comprehensive technical reference manual:

👉 **[https://geophilo.com/myface2city/](https://geophilo.com/myface2city/)**

Upload any portrait photo, choose from 10 curated artistic presets, and export scalable SVG posters directly in your browser.

---

## 📖 Overview

**`MyFace2City`** is a pure-Python generative cartography and optical portrait engine. It turns road networks, building footprints, land-use boundaries, and vector parcels into live optical portraits.

By binding a raster face/portrait photo to a geographic frame, each vector feature samples underlying image luminance and receives a reversible, rule-based cartographic style—without mutating source geometries or attributes.

Beyond the map-locked engine, the package ships a large collection of standalone **algorithmic art generators** (halftone rosettes, stippling, dithering, suminagashi marbling, stained glass, cyanotypes, voxel cityscapes, and more) that turn any raster image into vector SVG artwork, plus a Wavefront `.OBJ` 3D relief exporter.

---

## ✨ Features

- 🎭 **UrbanPortrait Engine:** Live luminance sampling with distortion-free aspect-ratio fitting and reversible feature styling.
- 🎨 **10 Curated Art Presets:** Ink Portrait, Neon Night, Blueprint, Sepia Blocks, Negative City, Cyberpunk 2077, Vintage Engraving, Thermal Heatmap, Emerald Eco-Map, and Nordic Slate.
- 🔘 **Algorithmic Halftone & Vector Stippling:** Generates variable-radius engraving dot grids across geographic regions.
- 🖨️ **Print-Art Pipelines:** CMYK screen separation plates, Risograph dual-drum prints, and 4-colour offset CMYK rosette halftones.
- 🧵 **Generative Vector Art:** Flow-field streamlines, cross-hatching, Voronoi (CVT) mosaics, ASCII typographic grids, isometric voxel/city scenes, and reaction-diffusion patterns.
- 🎚️ **Tone & Dithering Toolkit:** Bayer ordered dithering, Floyd–Steinberg/Atkinson error diffusion, bilateral filtering, and CLAHE contrast enhancement.
- 🏛️ **Material Simulations:** Cyanotype blueprints, cathedral stained glass, wood marquetry, Suminagashi marbling, watercolour washes, linocut, origami papercraft, thermal-infrared heatmaps, and tactile 3D relief meshes.
- 🗺️ **OpenStreetMap Acquisition (Overpass API):** Built-in client to fetch roads and buildings for any bounding box, with an offline synthetic grid fallback.
- 🖼️ **Standalone Scalable Vector SVG Exporter:** Generates high-resolution SVG posters with dark/light themes and glowing underlays.
- ⚙️ **Smart Image Enhancement:** Automatic histogram quantile contrast stretching, gamma correction, inversion, and edge emphasis.
- 💻 **CLI Interface:** Fast command-line rendering (`myface2city render`, `myface2city stipple`, `myface2city presets`).

---

## 🚀 Quick Start

### Installation

Install the runtime package from PyPI (only depends on [Pillow](https://pypi.org/project/pillow/)):

```bash
pip install myface2city
```

Install the development extras (test + lint + release tooling):

```bash
pip install -e ".[dev]"
```

Or install directly from a source checkout:

```bash
git clone https://gitlab.com/geospacephilo/MyFace2City.git
cd MyFace2City
pip install -e ".[dev]"
```

`myface2city` requires **Python 3.9+** and ships a `py.typed` marker for full type-checker support.

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

> **Working offline?** Swap `mfc.fetch_osm_network(bounds)` for
> `mfc.generate_synthetic_urban_grid(bounds)` to build with a deterministic demo street grid.

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

### Generative Art Generators

Every generator accepts an image (a path or a `PIL.Image`) and returns an artwork object
that renders itself with `to_svg()` and saves with `save_svg(path)`:

```python
from PIL import Image
import myface2city as mfc

img = Image.open("face.jpg")

# Flow-field streamlines guided by image gradients
mfc.generate_flow_field_art(img, num_particles=1500).save_svg("flow.svg")

# 4-colour offset CMYK rosette halftone
mfc.generate_cmyk_rosette_portrait(img).save_svg("rosette.svg")

# Japanese Suminagashi marbling with hydrodynamic vortices
mfc.generate_suminagashi_marbling_portrait(img).save_svg("marbling.svg")

# 2.5D isometric voxel cityscape
mfc.generate_isometric_voxel_art(img).save_svg("voxels.svg")

# Voronoi (CVT) mosaic, also exportable as GeoJSON
voronoi = mfc.generate_voronoi_stipple(img, target_points=400)
voronoi.to_svg()
voronoi.to_geojson()
```

### 3D Relief Mesh Export

```python
from PIL import Image
import myface2city as mfc

mesh = mfc.generate_3d_relief_mesh(Image.open("face.jpg"), grid_size=64, max_height=20.0)
mesh.save_obj("relief.obj")  # Wavefront .OBJ with vertices, normals, and UVs
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

Both `render` and `stipple` write `.geojson` output when the `--output` path ends in `.geojson`,
and `.svg` otherwise. When no `--vector` or `--osm-bbox` is supplied, `render` falls back to a
synthetic street network so you can preview artwork offline.

---

## 📚 Public API Reference

### Core Engine & Presets

| Symbol | Description |
| --- | --- |
| `UrbanPortrait(image_source, bounds, config=None)` | Map-locked engine binding an image to geographic bounds; exposes `sample_point`, `sample_pixel`, `sample_geometry`, `style_feature`, and `process_geojson`. |
| `RenderConfig(preset="Ink Portrait", sampling="balanced", gamma=1.0, invert=False, auto_contrast=True, clip_fraction=0.01, edge_amount=0.0, max_features=50000, opacity=1.0)` | Tone-processing and sampling configuration for `UrbanPortrait`. |
| `Palette(name, colors, background, widths, hide_highlights=False)` | Immutable 5-tone colorway and styling configuration. |
| `PRESETS` | Mapping of the 10 built-in preset names to `Palette` objects. |
| `get_preset(name)` / `list_presets()` | Look up a preset by exact or case-insensitive name / list all preset names. |
| `load_custom_palette(file_path)` / `save_custom_palette(palette, file_path)` | Read/write a `Palette` from/to a JSON file. |
| `NormalizedPoint(u, v)` | Image coordinate normalized to the inclusive `0.0 .. 1.0` range. |

### Profile & Tone Mathematics

| Symbol | Description |
| --- | --- |
| `fit_bounds_to_aspect(bounds, aspect_ratio)` | Fit the largest undistorted frame of the given aspect ratio inside a bounding box. |
| `map_to_normalized(x, y, bounds)` | Map a world coordinate to normalized image space (returns `None` outside the bounds). |
| `adjust_luminance(value, low=0.0, high=255.0, gamma=1.0, invert=False)` | Stretch, gamma-correct, and optionally invert an 8-bit luminance value. |
| `quantile_limits(histogram, clip_fraction=0.01)` | Robust low/high histogram limits for automatic contrast stretching. |
| `blend_edge(luminance, edge_strength, amount)` | Darken edges while preserving underlying tonal luminance. |

### Stippling, Export & Data Acquisition

| Symbol | Description |
| --- | --- |
| `calculate_stipple_points(min_x, min_y, max_x, max_y, grid_cols, grid_rows, sample_fn, max_radius=5.0, gamma=1.0, invert=False, preset="Ink Portrait")` | Build variable-radius halftone stipple dots from a sampling callback. |
| `stipple_to_geojson(points)` | Convert stipple points to a GeoJSON `FeatureCollection`. |
| `render_svg_artwork(geojson_data, bounds=None, preset="Ink Portrait", svg_width=1200, svg_height=1200, margin=40)` | Render styled features into a standalone SVG string. |
| `export_svg(geojson_data, output_path, preset="Ink Portrait", width=1200, height=1200)` | Render and write an SVG file, returning the written `Path`. |
| `fetch_osm_network(bbox, network_type="all", timeout=25)` | Fetch OSM roads/buildings for a bounding box via the Overpass API. |
| `generate_synthetic_urban_grid(bbox=(27.1, 38.4, 27.15, 38.45), grid_density=15)` | Build a deterministic synthetic road grid and parcel set for offline use. |

### Art Generators

Each generator returns its matching artwork object, which provides `to_svg()` and `save_svg(path)`.

| Generator | Returns | Description |
| --- | --- | --- |
| `generate_voronoi_stipple(image, preset="Ink Portrait", target_points=400, iterations=5)` | `VoronoiArtwork` | Centroidal Voronoi (CVT) mosaic; also exports GeoJSON. |
| `generate_3d_relief_mesh(image, grid_size=64, max_height=20.0, base_thickness=2.0, invert_height=True)` | `ReliefMesh3D` | 3D extruded relief surface, exportable as Wavefront `.OBJ`. |
| `generate_flow_field_art(image, num_particles=1500, step_length=3.0, max_steps=40, noise_scale=0.02)` | `FlowFieldArtwork` | Streamlines traced along luminance/edge gradients. |
| `generate_cmyk_screen_layers(image, grid_cells_x=50)` | `ColorSeparationArtwork` | CMYK separation plates for screen printing. |
| `generate_isometric_voxel_art(image, grid_resolution=32, max_height_voxels=16, block_width=16.0)` | `VoxelScene` | 2.5D isometric voxel blocks with shaded faces. |
| `bilateral_texture_filter(image, spatial_sigma=3.0, range_sigma=30.0)` | `PIL.Image` | Edge-preserving bilateral smoothing. |
| `clahe_contrast_enhancer(image, clip_limit=2.0)` | `PIL.Image` | Local contrast enhancement. |
| `generate_ascii_map_art(image, cols=80, char_palette=" .:-=+*#%@", invert_luminance=False)` | `ASCIIArtwork` | Character-density typographic portrait; `to_plain_text()` / `to_html()` / `save_html()`. |
| `generate_turing_portrait(image, resolution=48, iterations=30)` | `TuringPatternArtwork` | Reaction-diffusion Turing pattern portrait. |
| `simulate_gray_scott(width, height, feed_matrix, kill_matrix, iterations=25, da=1.0, db=0.5, dt=1.0)` | `list[list[float]]` | Solve the Gray-Scott reaction-diffusion PDE, returning the chemical-B field. |
| `generate_engraved_hatching_art(image, grid_step_px=6, hatch_angles_deg=(45.0, -45.0, 0.0), luminance_thresholds=(0.75, 0.50, 0.25))` | `HatchingArtwork` | Multi-pass pen & ink cross-hatching. |
| `generate_ordered_dither_portrait(image, scale_factor=1.0)` | `DitherArtwork` | Bayer 4×4 ordered matrix dithering. |
| `apply_error_diffusion_dither(image, method="floyd_steinberg")` | `DitherArtwork` | Floyd–Steinberg or Atkinson error diffusion. |
| `generate_isometric_city_portrait(image, grid_size=16, max_building_height_voxels=12, palette_top="#38bdf8", palette_left="#0284c7", palette_right="#0369a1")` | `IsometricCityArtwork` | Axonometric skyscraper cityscape. |
| `apply_watercolor_wash_portrait(image, params=None, grid_step_px=6)` | `WatercolorArtwork` | Fluid watercolour washes with pigment bleeds. |
| `generate_linocut_portrait(image, params=None)` | `LinocutArtwork` | Woodblock/linocut relief grooves. |
| `generate_stained_glass_portrait(image, tile_size_px=12, lead_came_width_px=2.5, glass_palette=...)` | `StainedGlassArtwork` | Luminous glass facets with lead cames. |
| `generate_blueprint_portrait(image, params=None)` | `CyanotypeArtwork` | Prussian-blue cyanotype drafting schematic. |
| `generate_cyberpunk_neon_portrait(image, palette=None, grid_horizon_ratio=0.65)` | `CyberpunkArtwork` | Synthwave neon vectors with glow filters. |
| `generate_marquetry_portrait(image, tile_size_px=4, palette=None)` | `MarquetryArtwork` | Wood-inlay parquet mosaic with species histogram. |
| `generate_thermal_infrared_portrait(image, min_temp_c=24.0, max_temp_c=37.5, palette=None, pixel_bin_size_px=2)` | `ThermalInfraredArtwork` | FLIR Ironbow false-colour heatmap. |
| `generate_origami_papercraft_portrait(image, grid_subdivision_px=6, paper_base_color_hex="#f0ebe1")` | `OrigamiArtwork` | Faceted low-poly papercraft tessellation. |
| `generate_risograph_print_portrait(image, dot_pitch_px=4, drum_1=None, drum_2=None, paper_tone_hex="#faf6ed")` | `RisographArtwork` | Dual-colour Risograph stencil print with misregistration. |
| `generate_cmyk_rosette_portrait(image, screen_pitch_px=5, angles=None, paper_tone_hex="#ffffff")` | `HalftoneRosetteArtwork` | 4-colour offset CMYK angled halftone rosette. |
| `generate_suminagashi_marbling_portrait(image, params=None, grid_step_px=5)` | `SuminagashiArtwork` | Japanese floating-ink marbling with vortices. |

Related configuration/result dataclasses are exported alongside each generator:
`VoronoiCell`, `Streamline`, `ScreenPrintPlate`, `VoxelBlock`, `HatchingStroke`, `IsometricVoxel`,
`WatercolorPigmentParams`, `LinocutCarveParams`, `GlassFacet`, `BlueprintGridParams`, `NeonPalette`,
`WoodSpeciesPalette`, `FLIRPalette`, `PaperFacetMesh`, `RisoColorDrum`, `RosetteScreenAngles`,
and `MarblingVortexParams`.

---

## 🛠️ Development

```bash
# Install dev extras
pip install -e ".[dev]"

# Run the test suite
python -m pytest -q

# Format and lint
python -m ruff format src tests
python -m ruff check .
```

See [`examples/cookbook.py`](examples/cookbook.py) for a runnable tour of the generators.

---

## 📜 License

MIT License © 2026 [Yusuf Eminoğlu](https://github.com/YusufEminoglu).
