# -*- coding: utf-8 -*-
"""Unit tests for Voronoi mosaic art and 3D relief mesh modules in myface2city."""

from __future__ import annotations

import tempfile
from pathlib import Path
from PIL import Image

from myface2city import (
    ReliefMesh3D,
    VoronoiArtwork,
    generate_3d_relief_mesh,
    generate_voronoi_stipple,
)


def _create_sample_image(width: int = 100, height: int = 100) -> Image.Image:
    """Generate simple synthetic gradient/circle image."""
    img = Image.new("L", (width, height), color=255)
    pixels = img.load()
    for x in range(width):
        for y in range(height):
            # Center dark circle
            dx = x - width / 2.0
            dy = y - height / 2.0
            if dx * dx + dy * dy < 25.0 * 25.0:
                pixels[x, y] = 30
            else:
                pixels[x, y] = int(200 + 55 * (x / width))
    return img


def test_voronoi_stipple_generation_and_export():
    img = _create_sample_image(80, 80)
    artwork = generate_voronoi_stipple(img, preset="Ink Portrait", target_points=50, iterations=2)

    assert isinstance(artwork, VoronoiArtwork)
    assert artwork.width == 80
    assert artwork.height == 80
    assert len(artwork.cells) > 0

    svg_str = artwork.to_svg()
    assert "<svg" in svg_str
    assert "polygon" in svg_str

    fc = artwork.to_geojson()
    assert fc["type"] == "FeatureCollection"
    assert len(fc["features"]) == len(artwork.cells)


def test_3d_relief_mesh_generation_and_obj_export():
    img = _create_sample_image(50, 50)
    mesh = generate_3d_relief_mesh(img, grid_size=20, max_height=10.0, base_thickness=1.0)

    assert isinstance(mesh, ReliefMesh3D)
    assert len(mesh.vertices) == 20 * 20
    assert len(mesh.faces) == (20 - 1) * (20 - 1) * 2

    obj_str = mesh.to_obj()
    assert "# MyFace2City 3D Relief Mesh Exporter" in obj_str
    assert "v " in obj_str
    assert "f " in obj_str

    with tempfile.TemporaryDirectory() as tmpdir:
        out_obj = Path(tmpdir) / "relief.obj"
        mesh.save_obj(out_obj)
        assert out_obj.exists()
        assert out_obj.stat().st_size > 100
