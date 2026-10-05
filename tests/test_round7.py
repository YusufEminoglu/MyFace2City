# -*- coding: utf-8 -*-
"""Unit tests for myface2city Round 7 features (Linocut Art & Stained Glass Mosaic)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from PIL import Image

from myface2city import (
    LinocutArtwork,
    LinocutCarveParams,
    StainedGlassArtwork,
    generate_linocut_portrait,
    generate_stained_glass_portrait,
)


class TestMyFace2CityRound7(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.tmp = Path(self.temp_dir.name)

        self.test_img = Image.new("L", (24, 24), color=110)
        for x in range(24):
            for y in range(24):
                self.test_img.putpixel((x, y), int((x * 10 + y * 5) % 255))

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_linocut_woodblock_portrait(self) -> None:
        params = LinocutCarveParams(line_spacing_px=4, carve_angle_degrees=30.0)
        art = generate_linocut_portrait(self.test_img, params=params)

        self.assertIsInstance(art, LinocutArtwork)
        self.assertEqual(art.width, 24)
        self.assertEqual(art.height, 24)
        self.assertGreater(art.groove_count, 0)

        svg = art.to_svg()
        self.assertIn("linocut-grooves", svg)

        svg_path = self.tmp / "linocut.svg"
        art.save_svg(svg_path)
        self.assertTrue(svg_path.exists())

    def test_cathedral_stained_glass_mosaic(self) -> None:
        art = generate_stained_glass_portrait(self.test_img, tile_size_px=6, lead_came_width_px=2.0)

        self.assertIsInstance(art, StainedGlassArtwork)
        self.assertGreater(art.facets_count, 0)
        self.assertEqual(len(art.facets), art.facets_count)

        svg = art.to_svg()
        self.assertIn("stained-glass-mosaic", svg)
        self.assertIn("<polygon", svg)

        svg_path = self.tmp / "stained_glass.svg"
        art.save_svg(svg_path)
        self.assertTrue(svg_path.exists())
