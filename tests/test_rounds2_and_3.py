# -*- coding: utf-8 -*-
"""Unit tests for myface2city Rounds 2 and 3 features (Flow Field, CMYK Separation, Voxel Art, Tone Filter)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from PIL import Image

from myface2city import (
    ColorSeparationArtwork,
    FlowFieldArtwork,
    VoxelScene,
    bilateral_texture_filter,
    clahe_contrast_enhancer,
    generate_cmyk_screen_layers,
    generate_flow_field_art,
    generate_isometric_voxel_art,
)


class TestMyFace2CityRounds2And3(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.tmp = Path(self.temp_dir.name)

        # Create a gradient test image (64x64)
        self.test_img = Image.new("RGB", (64, 64), color="white")
        for x in range(64):
            for y in range(64):
                val = int((x + y) * 2)
                self.test_img.putpixel((x, y), (val, val, val))

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_flow_field_generation(self) -> None:
        art = generate_flow_field_art(self.test_img, num_particles=100, max_steps=20)
        self.assertIsInstance(art, FlowFieldArtwork)
        self.assertEqual(art.width, 64)
        self.assertGreater(len(art.streamlines), 0)

        svg = art.to_svg()
        self.assertIn("<svg", svg)
        self.assertIn("<path", svg)

    def test_cmyk_screen_layers(self) -> None:
        sep = generate_cmyk_screen_layers(self.test_img, grid_cells_x=20)
        self.assertIsInstance(sep, ColorSeparationArtwork)
        self.assertEqual(len(sep.plates), 4)

        plates_dir = self.tmp / "plates"
        saved = sep.export_plates_svg(plates_dir, cell_size=8)
        self.assertEqual(len(saved), 4)
        self.assertTrue(all(p.exists() for p in saved))

    def test_isometric_voxel_art(self) -> None:
        scene = generate_isometric_voxel_art(self.test_img, grid_resolution=16)
        self.assertIsInstance(scene, VoxelScene)
        self.assertEqual(len(scene.blocks), 256)

        svg = scene.to_svg()
        self.assertIn("<svg", svg)
        self.assertIn("<polygon", svg)

    def test_bilateral_and_clahe_filters(self) -> None:
        filtered = bilateral_texture_filter(self.test_img, spatial_sigma=2.0, range_sigma=20.0)
        self.assertIsInstance(filtered, Image.Image)
        self.assertEqual(filtered.size, (64, 64))

        enhanced = clahe_contrast_enhancer(self.test_img, clip_limit=2.0)
        self.assertIsInstance(enhanced, Image.Image)
