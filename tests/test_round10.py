# -*- coding: utf-8 -*-
"""Unit tests for myface2city Round 10 features (Origami Papercraft & Risograph Print)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from PIL import Image

from myface2city import (
    OrigamiArtwork,
    RisoColorDrum,
    RisographArtwork,
    generate_origami_papercraft_portrait,
    generate_risograph_print_portrait,
)


class TestMyFace2CityRound10(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.tmp = Path(self.temp_dir.name)
        # Create small test image
        self.img = Image.new("L", (24, 24), color=120)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_origami_papercraft(self) -> None:
        art = generate_origami_papercraft_portrait(self.img, grid_subdivision_px=6)

        self.assertIsInstance(art, OrigamiArtwork)
        self.assertEqual(art.width, 24)
        self.assertEqual(art.height, 24)
        self.assertGreater(art.facets_count, 0)
        self.assertIn("origami-papercraft-mesh", art.to_svg())

        out_path = self.tmp / "origami.svg"
        art.save_svg(out_path)
        self.assertTrue(out_path.exists())

    def test_risograph_two_tone(self) -> None:
        d1 = RisoColorDrum("Fluo Orange", "#ff6b00")
        d2 = RisoColorDrum("Teal", "#00838a")

        art = generate_risograph_print_portrait(self.img, dot_pitch_px=4, drum_1=d1, drum_2=d2)

        self.assertIsInstance(art, RisographArtwork)
        self.assertEqual(art.width, 24)
        self.assertGreater(art.drum_1_dots_count, 0)
        self.assertIn("riso-drum-1", art.to_svg())

        out_path = self.tmp / "riso.svg"
        art.save_svg(out_path)
        self.assertTrue(out_path.exists())
