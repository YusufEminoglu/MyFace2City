# -*- coding: utf-8 -*-
"""Unit tests for myface2city Round 8 features (Cyanotype Blueprint & Cyberpunk Neon)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from PIL import Image

from myface2city import (
    BlueprintGridParams,
    CyanotypeArtwork,
    CyberpunkArtwork,
    NeonPalette,
    generate_blueprint_portrait,
    generate_cyberpunk_neon_portrait,
)


class TestMyFace2CityRound8(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.tmp = Path(self.temp_dir.name)

        self.test_img = Image.new("L", (32, 32), color=128)
        for x in range(32):
            for y in range(32):
                self.test_img.putpixel((x, y), int((x * 8 + y * 8) % 255))

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_cyanotype_blueprint_portrait(self) -> None:
        params = BlueprintGridParams(grid_spacing_px=16, frame_border_width_px=8)
        art = generate_blueprint_portrait(self.test_img, params=params)

        self.assertIsInstance(art, CyanotypeArtwork)
        self.assertEqual(art.width, 32)
        self.assertEqual(art.height, 32)
        self.assertGreater(art.drafting_elements_count, 0)

        svg = art.to_svg()
        self.assertIn("blueprint-schematics", svg)

        svg_path = self.tmp / "blueprint.svg"
        art.save_svg(svg_path)
        self.assertTrue(svg_path.exists())

    def test_cyberpunk_neon_portrait(self) -> None:
        art = generate_cyberpunk_neon_portrait(self.test_img)

        self.assertIsInstance(art, CyberpunkArtwork)
        self.assertGreater(art.neon_vectors_count, 0)

        svg = art.to_svg()
        self.assertIn("cyberpunk-neon-vectors", svg)
        self.assertIn('filter id="glow"', svg)

        svg_path = self.tmp / "cyberpunk.svg"
        art.save_svg(svg_path)
        self.assertTrue(svg_path.exists())
