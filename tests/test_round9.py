# -*- coding: utf-8 -*-
"""Unit tests for myface2city Round 9 features (Marquetry Wood Inlay & Thermal Infrared Art)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from PIL import Image

from myface2city import (
    MarquetryArtwork,
    ThermalInfraredArtwork,
    generate_marquetry_portrait,
    generate_thermal_infrared_portrait,
)


class TestMyFace2CityRound9(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.tmp = Path(self.temp_dir.name)

        self.test_img = Image.new("L", (24, 24), color=130)
        for x in range(24):
            for y in range(24):
                self.test_img.putpixel((x, y), int((x * 10 + y * 10) % 255))

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_marquetry_wood_inlay_art(self) -> None:
        art = generate_marquetry_portrait(self.test_img, tile_size_px=4)

        self.assertIsInstance(art, MarquetryArtwork)
        self.assertEqual(art.width, 24)
        self.assertEqual(art.height, 24)
        self.assertGreater(art.parquet_tiles_count, 0)

        svg = art.to_svg()
        self.assertIn("marquetry-wood-inlay", svg)

        svg_path = self.tmp / "marquetry.svg"
        art.save_svg(svg_path)
        self.assertTrue(svg_path.exists())

    def test_thermal_infrared_portrait(self) -> None:
        art = generate_thermal_infrared_portrait(self.test_img, min_temp_c=20.0, max_temp_c=38.0)

        self.assertIsInstance(art, ThermalInfraredArtwork)
        self.assertGreater(art.isotherms_count, 0)
        self.assertEqual(art.min_temperature_c, 20.0)

        svg = art.to_svg()
        self.assertIn("flir-thermal-infrared", svg)

        svg_path = self.tmp / "thermal.svg"
        art.save_svg(svg_path)
        self.assertTrue(svg_path.exists())
