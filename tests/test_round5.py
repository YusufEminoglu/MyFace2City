# -*- coding: utf-8 -*-
"""Unit tests for myface2city Round 5 features (Cross-Hatching & Matrix Dithering)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from PIL import Image

from myface2city import (
    DitherArtwork,
    HatchingArtwork,
    apply_error_diffusion_dither,
    generate_engraved_hatching_art,
    generate_ordered_dither_portrait,
)


class TestMyFace2CityRound5(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.tmp = Path(self.temp_dir.name)

        # Create test gradient image
        self.test_img = Image.new("L", (32, 32), color=128)
        for x in range(32):
            for y in range(32):
                self.test_img.putpixel((x, y), int((x + y) * 4))

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_engraved_cross_hatching(self) -> None:
        hatch = generate_engraved_hatching_art(self.test_img, grid_step_px=4)
        self.assertIsInstance(hatch, HatchingArtwork)
        self.assertEqual(hatch.width, 32)
        self.assertEqual(hatch.height, 32)
        self.assertGreater(len(hatch.strokes), 0)

        svg = hatch.to_svg()
        self.assertIn("<line", svg)

        svg_path = self.tmp / "hatch.svg"
        hatch.save_svg(svg_path)
        self.assertTrue(svg_path.exists())

    def test_matrix_dithering(self) -> None:
        # Bayer ordered dithering
        bayer = generate_ordered_dither_portrait(self.test_img)
        self.assertIsInstance(bayer, DitherArtwork)
        self.assertEqual(bayer.dither_algorithm, "Bayer_4x4")
        img_bayer = bayer.to_image()
        self.assertEqual(img_bayer.size, (32, 32))

        # Floyd-Steinberg error diffusion
        floyd = apply_error_diffusion_dither(self.test_img, method="floyd_steinberg")
        self.assertIsInstance(floyd, DitherArtwork)
        self.assertEqual(len(floyd.dither_matrix), 32)
        self.assertEqual(len(floyd.dither_matrix[0]), 32)

        # Atkinson error diffusion
        atkinson = apply_error_diffusion_dither(self.test_img, method="atkinson")
        self.assertIsInstance(atkinson, DitherArtwork)
        self.assertEqual(atkinson.dither_algorithm, "atkinson")
