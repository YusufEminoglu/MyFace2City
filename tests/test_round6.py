# -*- coding: utf-8 -*-
"""Unit tests for myface2city Round 6 features (Isometric Cityscape & Watercolor Washes)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from PIL import Image

from myface2city import (
    IsometricCityArtwork,
    WatercolorArtwork,
    WatercolorPigmentParams,
    apply_watercolor_wash_portrait,
    generate_isometric_city_portrait,
)


class TestMyFace2CityRound6(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.tmp = Path(self.temp_dir.name)

        self.test_img = Image.new("L", (16, 16), color=120)
        for x in range(16):
            for y in range(16):
                self.test_img.putpixel((x, y), int((x * y) % 255))

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_isometric_city_portrait(self) -> None:
        iso = generate_isometric_city_portrait(self.test_img, grid_size=8, max_building_height_voxels=10)

        self.assertIsInstance(iso, IsometricCityArtwork)
        self.assertEqual(len(iso.voxels), 64)
        self.assertGreater(iso.width, 0)
        self.assertGreater(iso.height, 0)

        svg = iso.to_svg()
        self.assertIn("<polygon", svg)

        svg_path = self.tmp / "iso.svg"
        iso.save_svg(svg_path)
        self.assertTrue(svg_path.exists())

    def test_watercolor_wash_portrait(self) -> None:
        params = WatercolorPigmentParams(bleed_radius_px=4)
        art = apply_watercolor_wash_portrait(self.test_img, params=params, grid_step_px=4)

        self.assertIsInstance(art, WatercolorArtwork)
        self.assertEqual(art.width, 16)
        self.assertEqual(art.height, 16)
        self.assertGreater(art.pigment_layers_count, 0)

        svg = art.to_svg()
        self.assertIn("feTurbulence", svg)
        self.assertIn("feDisplacementMap", svg)

        svg_path = self.tmp / "watercolor.svg"
        art.save_svg(svg_path)
        self.assertTrue(svg_path.exists())
