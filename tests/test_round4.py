# -*- coding: utf-8 -*-
"""Unit tests for myface2city Round 4 features (Typographic ASCII Art & Reaction-Diffusion)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from PIL import Image

from myface2city import (
    ASCIIArtwork,
    TuringPatternArtwork,
    generate_ascii_map_art,
    generate_turing_portrait,
    simulate_gray_scott,
)


class TestMyFace2CityRound4(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.tmp = Path(self.temp_dir.name)

        # Create gradient test image
        self.test_img = Image.new("L", (32, 32), color=128)
        for x in range(32):
            for y in range(32):
                self.test_img.putpixel((x, y), int((x + y) * 4))

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_ascii_art_generation(self) -> None:
        ascii_art = generate_ascii_map_art(self.test_img, cols=40)
        self.assertIsInstance(ascii_art, ASCIIArtwork)
        self.assertEqual(ascii_art.cols, 40)
        self.assertGreater(ascii_art.rows, 0)
        self.assertGreater(len(ascii_art.text_lines), 0)

        txt = ascii_art.to_plain_text()
        self.assertGreater(len(txt), 50)

        html_file = self.tmp / "portrait.html"
        ascii_art.save_html(html_file)
        self.assertTrue(html_file.exists())
        self.assertIn("<pre>", html_file.read_text(encoding="utf-8"))

    def test_reaction_diffusion_turing_patterns(self) -> None:
        feed = [[0.055] * 16 for _ in range(16)]
        kill = [[0.062] * 16 for _ in range(16)]
        b_mat = simulate_gray_scott(16, 16, feed, kill, iterations=10)
        self.assertEqual(len(b_mat), 16)
        self.assertEqual(len(b_mat[0]), 16)

        turing = generate_turing_portrait(self.test_img, resolution=24, iterations=15)
        self.assertIsInstance(turing, TuringPatternArtwork)
        self.assertEqual(turing.width, 24)

        img = turing.to_image()
        self.assertIsInstance(img, Image.Image)
        self.assertEqual(img.size, (24, 24))
