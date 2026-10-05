# -*- coding: utf-8 -*-
"""Unit tests for myface2city Round 11 features (CMYK Rosette Halftone & Suminagashi Marbling)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from PIL import Image

from myface2city import (
    HalftoneRosetteArtwork,
    MarblingVortexParams,
    SuminagashiArtwork,
    generate_cmyk_rosette_portrait,
    generate_suminagashi_marbling_portrait,
)


class TestMyFace2CityRound11(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.tmp = Path(self.temp_dir.name)
        self.img = Image.new("RGB", (25, 25), color=(100, 150, 200))

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_cmyk_rosette_halftone(self) -> None:
        art = generate_cmyk_rosette_portrait(self.img, screen_pitch_px=5)

        self.assertIsInstance(art, HalftoneRosetteArtwork)
        self.assertEqual(art.width, 25)
        self.assertGreater(art.cyan_dots_count, 0)
        self.assertGreater(art.magenta_dots_count, 0)
        self.assertIn("Cyan Plate", art.to_svg())

        out_path = self.tmp / "rosette.svg"
        art.save_svg(out_path)
        self.assertTrue(out_path.exists())

    def test_suminagashi_water_marbling(self) -> None:
        params = MarblingVortexParams(vortex_intensity=1.8, ink_color_hex="#0b132b")
        art = generate_suminagashi_marbling_portrait(self.img, params=params, grid_step_px=5)

        self.assertIsInstance(art, SuminagashiArtwork)
        self.assertEqual(art.width, 25)
        self.assertGreater(art.ink_streamlines_count, 0)
        self.assertGreater(art.marbled_vortices_count, 0)

        out_path = self.tmp / "marbling.svg"
        art.save_svg(out_path)
        self.assertTrue(out_path.exists())
