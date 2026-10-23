# -*- coding: utf-8 -*-
"""Edge-case and error-path tests for public myface2city APIs."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from PIL import Image

import myface2city as mfc
from myface2city.color_separation import generate_cmyk_screen_layers
from myface2city.dithering_matrix import (
    DitherArtwork,
    apply_error_diffusion_dither,
    generate_ordered_dither_portrait,
)
from myface2city.engine import RenderConfig, UrbanPortrait
from myface2city.export import export_svg, render_svg_artwork
from myface2city.flow_field import FlowFieldArtwork, Streamline
from myface2city.isometric_block_art import (
    IsometricCityArtwork,
    IsometricVoxel,
)
from myface2city.osm import _overpass_to_geojson, fetch_osm_network, generate_synthetic_urban_grid
from myface2city.presets import Palette, get_preset
from myface2city.relief import ReliefMesh3D
from myface2city.stipple import calculate_stipple_points
from myface2city.voronoi_art import VoronoiArtwork, VoronoiCell


def _gradient_image(size: int = 16) -> Image.Image:
    """Create a small deterministic grayscale gradient image."""
    img = Image.new("L", (size, size))
    pixels = img.load()
    for y in range(size):
        for x in range(size):
            pixels[x, y] = int(255 * (x + y) / (2 * (size - 1)))
    return img


def _save_png(tmp_path: Path, img: Image.Image) -> Path:
    """Save ``img`` as a PNG inside ``tmp_path`` and return the path."""
    path = tmp_path / "input.png"
    img.save(path)
    return path


# ---------------------------------------------------------------------------
# Stipple validation and tone paths
# ---------------------------------------------------------------------------


def test_stipple_rejects_invalid_arguments() -> None:
    """Every documented validation guard raises ValueError."""
    with pytest.raises(ValueError):
        calculate_stipple_points(0.0, 0.0, float("inf"), 1.0, 4, 4, lambda u, v: 0.0)
    with pytest.raises(ValueError):
        calculate_stipple_points(10.0, 0.0, 0.0, 1.0, 4, 4, lambda u, v: 0.0)
    with pytest.raises(ValueError):
        calculate_stipple_points(0.0, 0.0, 1.0, 1.0, 1, 4, lambda u, v: 0.0)
    with pytest.raises(ValueError):
        calculate_stipple_points(0.0, 0.0, 1.0, 1.0, 4, 4, lambda u, v: 0.0, max_radius=0.0)
    with pytest.raises(ValueError):
        calculate_stipple_points(0.0, 0.0, 1.0, 1.0, 4, 4, lambda u, v: 0.0, gamma=0.0)


def test_stipple_invert_gamma_and_radius_clipping() -> None:
    """Inversion flips dot presence, gamma scales radius, and white pixels are skipped."""
    bright = calculate_stipple_points(0.0, 0.0, 1.0, 1.0, 4, 4, lambda u, v: 0.0)
    assert len(bright) == 16
    assert all(pt["radius"] > 0.0 for pt in bright)

    inverted = calculate_stipple_points(0.0, 0.0, 1.0, 1.0, 4, 4, lambda u, v: 0.0, invert=True)
    assert inverted == []

    black = calculate_stipple_points(0.0, 0.0, 1.0, 1.0, 4, 4, lambda u, v: 255.0)
    assert black == []

    linear = calculate_stipple_points(0.0, 0.0, 1.0, 1.0, 4, 4, lambda u, v: 64.0, gamma=1.0)
    curved = calculate_stipple_points(0.0, 0.0, 1.0, 1.0, 4, 4, lambda u, v: 64.0, gamma=2.0)
    assert curved[0]["radius"] < linear[0]["radius"]


# ---------------------------------------------------------------------------
# Profile maths edge cases
# ---------------------------------------------------------------------------


def test_profile_rejects_degenerate_inputs() -> None:
    """Invalid bounds and aspect ratios raise ValueError."""
    with pytest.raises(ValueError):
        mfc.fit_bounds_to_aspect((0.0, 0.0, 0.0, 10.0), 1.0)
    with pytest.raises(ValueError):
        mfc.fit_bounds_to_aspect((0.0, 0.0, 10.0, 10.0), 0.0)


def test_profile_equal_ratio_and_normalization_edges() -> None:
    """A matching aspect ratio is returned unchanged and zero-size bounds are rejected."""
    bounds = (0.0, 0.0, 10.0, 10.0)
    assert mfc.fit_bounds_to_aspect(bounds, 1.0) == bounds
    assert mfc.map_to_normalized(1.0, 1.0, (0.0, 0.0, 0.0, 10.0)) is None
    assert isinstance(mfc.adjust_luminance(100, low=200.0, high=100.0), int)


def test_quantile_limits_degenerate_histograms() -> None:
    """Empty and single-valued histograms fall back to the full 0..255 range."""
    assert mfc.quantile_limits([0] * 256) == (0, 255)
    hist = [0] * 256
    hist[128] = 1000
    assert mfc.quantile_limits(hist, clip_fraction=0.01) == (0, 255)


# ---------------------------------------------------------------------------
# Presets fallbacks
# ---------------------------------------------------------------------------


def test_get_preset_unknown_name_falls_back_to_ink_portrait() -> None:
    """Unknown preset names resolve to the default Ink Portrait palette."""
    assert get_preset("does-not-exist").name == "Ink Portrait"
    assert get_preset("neon_night").name == "Neon Night"


def test_palette_from_dict_defaults_and_truncation() -> None:
    """Missing keys fall back to defaults and surplus tones are truncated."""
    palette = Palette.from_dict({})
    assert palette.name == "Custom"
    assert palette.colors == ("#000000",) * 5
    assert palette.widths == (1.0, 0.8, 0.6, 0.4, 0.2)
    assert palette.background == "#ffffff"
    assert palette.hide_highlights is False

    overfull = Palette.from_dict({"colors": ["#111111"] * 7, "widths": [1.0] * 7})
    assert len(overfull.colors) == 5
    assert len(overfull.widths) == 5
    assert Palette.from_dict(palette.to_dict(), name="RoundTrip").name == "Custom"


# ---------------------------------------------------------------------------
# UrbanPortrait branches
# ---------------------------------------------------------------------------


def test_urban_portrait_rejects_unsupported_source() -> None:
    """Non-image sources raise a clear TypeError."""
    with pytest.raises(TypeError):
        UrbanPortrait(123, (0.0, 0.0, 10.0, 10.0))  # type: ignore[arg-type]


def test_urban_portrait_sampling_and_config_branches() -> None:
    """Exercise clamped sampling, sampling modes, geometry types, and feature limits."""
    img = _gradient_image(16)
    bounds = (0.0, 0.0, 10.0, 10.0)
    portrait = UrbanPortrait(img, bounds, RenderConfig(auto_contrast=False))
    assert (portrait.low_limit, portrait.high_limit) == (0, 255)

    assert portrait.sample_pixel(-5.0, -5.0) == img.getpixel((0, 0))
    assert portrait.sample_pixel(5.0, 5.0) == img.getpixel((15, 15))
    assert portrait.sample_point(50.0, 50.0) is None

    point = {"type": "Point", "coordinates": [5.0, 5.0]}
    assert isinstance(portrait.sample_geometry(point), int)

    line = {"type": "LineString", "coordinates": [[1.0, 1.0], [5.0, 5.0], [9.0, 9.0]]}
    assert isinstance(portrait.sample_geometry(line), int)

    poly = {
        "type": "Polygon",
        "coordinates": [[[1.0, 1.0], [9.0, 1.0], [9.0, 9.0], [1.0, 9.0], [1.0, 1.0]]],
    }
    assert isinstance(portrait.sample_geometry(poly), int)
    assert portrait.sample_geometry({"type": "GeometryCollection"}) == 255
    assert portrait.sample_geometry({}) == 255

    for mode in ("center", "balanced", "high_quality"):
        portrait.config.sampling = mode
        assert isinstance(portrait.sample_geometry(line), int)

    features = [point, line, poly]
    portrait.config.max_features = 1
    styled = portrait.process_geojson({"type": "FeatureCollection", "features": features}, "Ink Portrait")
    assert len(styled["features"]) == 1


# ---------------------------------------------------------------------------
# Export branches
# ---------------------------------------------------------------------------


def test_render_svg_empty_point_and_hidden_features() -> None:
    """Empty collections, point features, polygons, and hidden features render safely."""
    empty_svg = render_svg_artwork({"type": "FeatureCollection", "features": []})
    assert empty_svg.startswith("<svg")

    styled = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [1.0, 2.0]},
                "properties": {"_portrait_color": "#ff0000", "_stroke_width": 3.0},
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0]]],
                },
                "properties": {},
            },
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [3.0, 3.0]},
                "properties": {"_is_hidden": True},
            },
        ],
    }
    svg = render_svg_artwork(styled, bounds=(0.0, 0.0, 10.0, 10.0), preset="Ink Portrait")
    assert "<circle" in svg
    assert "<path" in svg
    assert svg.count("<circle") == 1

    # When bounds are omitted, coordinates are inspected and the fallback frame is used.
    auto_svg = render_svg_artwork({"type": "FeatureCollection", "features": styled["features"][:1]})
    assert auto_svg.startswith("<svg")
    assert "<circle" in auto_svg


def test_export_svg_creates_parent_directories(tmp_path: Path) -> None:
    """Named export writes into nested, not-yet-existing directories."""
    target = tmp_path / "nested" / "art.svg"
    written = export_svg({"type": "FeatureCollection", "features": []}, target)
    assert written == target
    assert target.exists()


# ---------------------------------------------------------------------------
# Dithering and color separation branches
# ---------------------------------------------------------------------------


def test_dithering_path_inputs_and_scale() -> None:
    """Dithering accepts file paths, scales images, and supports Atkinson diffusion."""
    img = _gradient_image(16)
    artwork = generate_ordered_dither_portrait(img, scale_factor=0.5)
    assert (artwork.width, artwork.height) == (8, 8)

    atkinson = apply_error_diffusion_dither(img, method="atkinson")
    assert atkinson.dither_algorithm == "atkinson"
    assert len(atkinson.dither_matrix) == 16

    bitmap = atkinson.to_image()
    assert bitmap.mode == "1"
    assert bitmap.size == (16, 16)


def test_dithering_and_separation_accept_paths(tmp_path: Path) -> None:
    """Path-based image sources follow the same code path as PIL images."""
    path = _save_png(tmp_path, _gradient_image(12))
    assert generate_ordered_dither_portrait(path).width == 12
    assert apply_error_diffusion_dither(path).height == 12
    assert generate_cmyk_screen_layers(path, grid_cells_x=4).width == 12


def test_cmyk_pure_black_hits_key_channel_branch() -> None:
    """A pure black pixel produces full black plate coverage and zero CMY."""
    artwork = generate_cmyk_screen_layers(Image.new("RGB", (1, 1), (0, 0, 0)), grid_cells_x=1)
    channels = {plate.plate_name: plate.dot_radius_matrix[0][0] for plate in artwork.plates}
    assert channels["Black"] == 1.0
    assert channels["Cyan"] == 0.0
    assert channels["Magenta"] == 0.0
    assert channels["Yellow"] == 0.0


def test_dither_artwork_direct_construction() -> None:
    """A DitherArtwork can be built from an explicit bitmap and rendered to mode '1'."""
    art = DitherArtwork(width=2, height=1, dither_algorithm="custom", dither_matrix=[[0, 255]])
    bitmap = art.to_image()
    assert bitmap.size == (2, 1)
    assert bitmap.getpixel((0, 0)) == 0
    assert bitmap.getpixel((1, 0)) == 1


# ---------------------------------------------------------------------------
# Remaining generator path-input branches and exporters
# ---------------------------------------------------------------------------


def test_generators_accept_file_paths(tmp_path: Path) -> None:
    """All path-accepting generators load the image from disk correctly."""
    path = _save_png(tmp_path, _gradient_image(16))

    assert mfc.generate_ascii_map_art(path, cols=8).cols == 8
    assert mfc.generate_blueprint_portrait(path).width == 16
    assert mfc.generate_flow_field_art(path, num_particles=10, max_steps=3).width == 16
    assert mfc.generate_engraved_hatching_art(path, grid_step_px=4).width == 16
    assert mfc.generate_isometric_city_portrait(path, grid_size=4).width > 0
    assert mfc.generate_cyberpunk_neon_portrait(path).width == 16
    assert mfc.generate_turing_portrait(path, resolution=6, iterations=2).width == 6
    assert mfc.generate_stained_glass_portrait(path, tile_size_px=8).width == 16
    assert mfc.generate_linocut_portrait(path).width == 16
    assert mfc.apply_watercolor_wash_portrait(path, grid_step_px=8).width == 16
    assert mfc.generate_isometric_voxel_art(path, grid_resolution=4).grid_cols == 4
    assert mfc.bilateral_texture_filter(path, spatial_sigma=1.0, range_sigma=10.0).size == (16, 16)
    assert mfc.clahe_contrast_enhancer(path).size == (16, 16)


def test_ascii_exporters(tmp_path: Path) -> None:
    """Plain-text, HTML, and saved-HTML exporters emit non-empty content."""
    art = mfc.generate_ascii_map_art(_gradient_image(8), cols=6)
    assert len(art.to_plain_text().splitlines()) == art.rows
    assert "<html" in art.to_html()
    saved = art.save_html(tmp_path / "ascii.html")
    assert saved.exists() and saved.stat().st_size > 0


def test_flow_field_skips_short_streamlines_and_saves(tmp_path: Path) -> None:
    """Single-point streamlines are skipped and explicit stroke colours override defaults."""
    art = FlowFieldArtwork(
        width=10,
        height=10,
        streamlines=[Streamline(points=[(0.0, 0.0)], stroke_width=1.0, color_hex="#ffffff")],
    )
    svg = art.to_svg(stroke_color="#abcdef")
    assert "<path" not in svg
    assert "#abcdef" not in svg
    assert art.save_svg(tmp_path / "flow.svg").exists()


def test_isometric_artwork_skips_flat_voxels_and_saves(tmp_path: Path) -> None:
    """Zero-height voxels are omitted and the scene can be saved."""
    voxel = IsometricVoxel(
        grid_c=0,
        grid_r=0,
        height_voxels=0,
        iso_screen_x=10.0,
        iso_screen_y=10.0,
        top_color_hex="#111111",
        left_color_hex="#222222",
        right_color_hex="#333333",
    )
    art = IsometricCityArtwork(width=20, height=20, voxels=[voxel])
    svg = art.to_svg()
    assert "<polygon" not in svg
    assert art.save_svg(tmp_path / "iso.svg").exists()


def test_watercolor_skips_white_paper() -> None:
    """Near-white pixels are preserved as bare paper (no pigment blobs)."""
    art = mfc.apply_watercolor_wash_portrait(Image.new("L", (16, 16), 255), grid_step_px=4)
    assert art.pigment_layers_count == 0


def test_stained_marble_and_voxel_save(tmp_path: Path) -> None:
    """SVG save helpers write non-empty files for artworks with void save methods."""
    marble = mfc.generate_suminagashi_marbling_portrait(Image.new("L", (12, 12), 128), grid_step_px=4)
    assert "<svg" in marble.to_svg()
    assert marble.save_svg(tmp_path / "marble.svg") is None
    assert (tmp_path / "marble.svg").stat().st_size > 0

    voxels = mfc.generate_isometric_voxel_art(Image.new("L", (8, 8), 100), grid_resolution=4)
    assert voxels.save_svg(tmp_path / "voxels.svg").exists()


# ---------------------------------------------------------------------------
# Direct dataclass rendering branches
# ---------------------------------------------------------------------------


def test_relief_obj_face_formats() -> None:
    """OBJ faces adapt to the presence of UVs and normals."""
    base = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)]
    faces = [(1, 2, 3)]

    bare = ReliefMesh3D(vertices=base, faces=faces).to_obj()
    assert "f 1 2 3" in bare

    uv_only = ReliefMesh3D(vertices=base, faces=faces, uvs=[(0.0, 0.0)] * 3).to_obj()
    assert "f 1/1 2/2 3/3" in uv_only

    full = ReliefMesh3D(
        vertices=base,
        faces=faces,
        uvs=[(0.0, 0.0)] * 3,
        normals=[(0.0, 0.0, 1.0)] * 3,
    ).to_obj()
    assert "f 1/1/1 2/2/2 3/3/3" in full


def test_voronoi_skips_degenerate_cells() -> None:
    """Cells with fewer than three vertices are omitted from SVG and GeoJSON."""
    art = VoronoiArtwork(
        width=10,
        height=10,
        cells=[VoronoiCell(centroid=(1.0, 1.0), polygon=[(0.0, 0.0), (1.0, 1.0)], luminance=0.5)],
        palette=get_preset("Ink Portrait"),
    )
    assert "<polygon" not in art.to_svg()
    assert art.to_geojson()["features"] == []


# ---------------------------------------------------------------------------
# OpenStreetMap acquisition
# ---------------------------------------------------------------------------


class _FakeResponse:
    """Minimal context-manager response used to stub urlopen."""

    def __init__(self, payload: bytes) -> None:
        self._payload = payload

    def read(self) -> bytes:
        return self._payload

    def __enter__(self) -> _FakeResponse:
        return self

    def __exit__(self, *args: object) -> None:
        return None


def test_fetch_osm_network_success_and_queries(monkeypatch: pytest.MonkeyPatch) -> None:
    """Successful Overpass responses are parsed for every network type."""
    payload = json.dumps(
        {
            "elements": [
                {"type": "node", "id": 1, "lat": 38.40, "lon": 27.10},
                {"type": "node", "id": 2, "lat": 38.41, "lon": 27.11},
                {"type": "way", "id": 10, "nodes": [1, 2], "tags": {"highway": "primary"}},
            ]
        }
    ).encode("utf-8")

    monkeypatch.setattr(
        "myface2city.osm.urllib.request.urlopen",
        lambda *args, **kwargs: _FakeResponse(payload),
    )
    for network_type in ("roads", "buildings", "all"):
        result = fetch_osm_network((27.10, 38.40, 27.12, 38.42), network_type=network_type)
        assert result["type"] == "FeatureCollection"
        assert len(result["features"]) == 1


def test_fetch_osm_network_rejects_oversized_bbox() -> None:
    """Bounding boxes larger than 100 km² are rejected before any network call."""
    with pytest.raises(ValueError):
        fetch_osm_network((0.0, 0.0, 10.0, 10.0))


def test_fetch_osm_network_raises_connection_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """When every Overpass server fails, a ConnectionError is raised."""
    monkeypatch.setattr(
        "myface2city.osm.urllib.request.urlopen",
        lambda *args, **kwargs: (_ for _ in ()).throw(OSError("offline")),
    )
    with pytest.raises(ConnectionError):
        fetch_osm_network((27.10, 38.40, 27.12, 38.42))


def test_overpass_parser_skips_incomplete_ways() -> None:
    """Ways with fewer than two resolved nodes are dropped."""
    parsed = _overpass_to_geojson(
        {
            "elements": [
                {"type": "node", "id": 1, "lat": 1.0, "lon": 2.0},
                {"type": "way", "id": 5, "nodes": [1, 99], "tags": {}},
            ]
        }
    )
    assert parsed == {"type": "FeatureCollection", "features": []}


def test_synthetic_grid_defaults() -> None:
    """The synthetic grid exposes roads and parcels for the default bounding box."""
    grid = generate_synthetic_urban_grid(grid_density=2)
    assert grid["type"] == "FeatureCollection"
    assert len(grid["features"]) == (2 + 1) * 2 + 2 * 2


# ---------------------------------------------------------------------------
# CLI error paths
# ---------------------------------------------------------------------------


def test_cli_missing_image_returns_error(capsys: pytest.CaptureFixture[str]) -> None:
    """Missing input images yield exit code 1 for render and stipple."""
    assert mfc.cli.main(["render", "--image", "definitely-missing.png"]) == 1
    assert mfc.cli.main(["stipple", "--image", "definitely-missing.png"]) == 1
    assert "not found" in capsys.readouterr().err.lower()


def test_cli_missing_vector_returns_error(tmp_path: Path) -> None:
    """A missing --vector file yields exit code 1."""
    image_path = _save_png(tmp_path, _gradient_image(8))
    code = mfc.cli.main(
        [
            "render",
            "--image",
            str(image_path),
            "--vector",
            str(tmp_path / "missing.geojson"),
            "--output",
            str(tmp_path / "out.svg"),
        ]
    )
    assert code == 1


def test_cli_stipple_writes_geojson(tmp_path: Path) -> None:
    """Stipple output honours a .geojson extension."""
    image_path = _save_png(tmp_path, _gradient_image(8))
    output_path = tmp_path / "stipple.geojson"
    code = mfc.cli.main(
        [
            "stipple",
            "--image",
            str(image_path),
            "--cols",
            "4",
            "--rows",
            "4",
            "--output",
            str(output_path),
        ]
    )
    assert code == 0
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["type"] == "FeatureCollection"


def test_cli_render_with_vector_file(tmp_path: Path) -> None:
    """A local GeoJSON vector file can drive the render command."""
    image_path = _save_png(tmp_path, _gradient_image(8))
    vector_path = tmp_path / "roads.geojson"
    vector_path.write_text(
        json.dumps(
            {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "geometry": {"type": "LineString", "coordinates": [[10.0, 10.0], [90.0, 90.0]]},
                        "properties": {},
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    output_path = tmp_path / "vector_render.svg"
    code = mfc.cli.main(
        ["render", "--image", str(image_path), "--vector", str(vector_path), "--output", str(output_path)]
    )
    assert code == 0
    assert output_path.exists()


def test_cli_render_osm_failure_falls_back(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """A failing Overpass fetch falls back to the synthetic grid instead of aborting."""
    image_path = _save_png(tmp_path, _gradient_image(8))

    def _boom(*args: object, **kwargs: object) -> dict:
        raise RuntimeError("overpass unavailable")

    monkeypatch.setattr("myface2city.cli.fetch_osm_network", _boom)
    output_path = tmp_path / "fallback.svg"
    code = mfc.cli.main(
        [
            "render",
            "--image",
            str(image_path),
            "--osm-bbox",
            "27.10,38.40,27.12,38.42",
            "--output",
            str(output_path),
        ]
    )
    assert code == 0
    assert output_path.exists()
