"""Comprehensive test suite for MyFace2City."""

import os
import tempfile
import unittest

from PIL import Image, ImageDraw

import myface2city
from myface2city.osm import _overpass_to_geojson


class TestMyFace2City(unittest.TestCase):
    def setUp(self) -> None:
        # Create a test gradient image (100x100)
        self.img = Image.new("L", (100, 100), color=255)
        draw = ImageDraw.Draw(self.img)
        draw.rectangle([20, 20, 80, 80], fill=50)  # Dark center
        draw.ellipse([35, 35, 65, 65], fill=0)  # Pure black center

        self.bounds = (27.10, 38.40, 27.20, 38.50)

    def test_profile_math(self) -> None:
        # Aspect fitting
        fitted = myface2city.fit_bounds_to_aspect((0.0, 0.0, 200.0, 100.0), 1.0)
        self.assertEqual(fitted[1], 0.0)
        self.assertEqual(fitted[3], 100.0)
        self.assertAlmostEqual(fitted[0], 50.0)
        self.assertAlmostEqual(fitted[2], 150.0)

        # Coordinate normalization
        norm = myface2city.map_to_normalized(50.0, 50.0, (0.0, 0.0, 100.0, 100.0))
        self.assertIsNotNone(norm)
        self.assertAlmostEqual(norm.u, 0.5)
        self.assertAlmostEqual(norm.v, 0.5)

        # Outside bounds
        norm_out = myface2city.map_to_normalized(150.0, 50.0, (0.0, 0.0, 100.0, 100.0))
        self.assertIsNone(norm_out)

        # Tone adjustment
        adj = myface2city.adjust_luminance(128, low=0, high=255, gamma=1.0, invert=False)
        self.assertEqual(adj, 128)
        adj_inv = myface2city.adjust_luminance(128, low=0, high=255, gamma=1.0, invert=True)
        self.assertEqual(adj_inv, 127)

        # Quantile limits
        hist = [0] * 256
        hist[50] = 500
        hist[200] = 500
        low, high = myface2city.quantile_limits(hist, clip_fraction=0.05)
        self.assertEqual(low, 50)
        self.assertEqual(high, 200)

        # Edge blending
        edge = myface2city.blend_edge(200, 255, 0.5)
        self.assertLessEqual(edge, 200)

    def test_presets(self) -> None:
        presets = myface2city.list_presets()
        self.assertEqual(len(presets), 10)
        self.assertIn("Cyberpunk 2077", presets)

        p = myface2city.get_preset("cyberpunk2077")
        self.assertEqual(p.name, "Cyberpunk 2077")
        self.assertEqual(len(p.colors), 5)

        # Custom palette save and load
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as tmp:
            tmp_path = tmp.name

        try:
            myface2city.save_custom_palette(p, tmp_path)
            loaded = myface2city.load_custom_palette(tmp_path)
            self.assertEqual(loaded.colors, p.colors)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_stipple_generator(self) -> None:
        def sample_fn(u: float, v: float) -> float:
            return 50.0

        points = myface2city.calculate_stipple_points(
            0.0,
            0.0,
            100.0,
            100.0,
            grid_cols=10,
            grid_rows=10,
            sample_fn=sample_fn,
            max_radius=5.0,
            preset="Ink Portrait",
        )
        self.assertEqual(len(points), 100)
        self.assertGreater(points[0]["radius"], 0.0)

        geojson = myface2city.stipple_to_geojson(points)
        self.assertEqual(len(geojson["features"]), 100)
        self.assertEqual(geojson["features"][0]["geometry"]["type"], "Point")

    def test_urban_portrait_engine(self) -> None:
        portrait = myface2city.UrbanPortrait(self.img, self.bounds)

        # Sample dark center (50, 50) in world coords -> (27.15, 38.45)
        luma_center = portrait.sample_point(27.15, 38.45)
        self.assertIsNotNone(luma_center)
        self.assertEqual(luma_center, 0)

        # Sample light corner (27.11, 38.41)
        luma_corner = portrait.sample_point(27.11, 38.41)
        self.assertIsNotNone(luma_corner)
        self.assertGreater(luma_corner, 200)

        # Process GeoJSON network
        grid = myface2city.generate_synthetic_urban_grid(self.bounds, grid_density=5)
        styled = portrait.process_geojson(grid, palette="Neon Night")
        self.assertIn("features", styled)
        self.assertGreater(len(styled["features"]), 0)

        first_feat = styled["features"][0]
        self.assertIn("_portrait_luminance", first_feat["properties"])
        self.assertIn("_portrait_color", first_feat["properties"])

    def test_svg_export(self) -> None:
        portrait = myface2city.UrbanPortrait(self.img, self.bounds)
        grid = myface2city.generate_synthetic_urban_grid(self.bounds, grid_density=4)
        styled = portrait.process_geojson(grid, palette="Blueprint")

        svg_str = myface2city.render_svg_artwork(styled, self.bounds, preset="Blueprint")
        self.assertTrue(svg_str.startswith("<svg"))
        self.assertIn("path", svg_str)

        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".svg") as tmp:
            tmp_path = tmp.name

        try:
            p = myface2city.export_svg(styled, tmp_path, preset="Blueprint")
            self.assertTrue(p.exists())
            self.assertGreater(p.stat().st_size, 100)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_overpass_parser(self) -> None:
        mock_osm = {
            "elements": [
                {"type": "node", "id": 1, "lat": 38.4, "lon": 27.1},
                {"type": "node", "id": 2, "lat": 38.5, "lon": 27.2},
                {"type": "node", "id": 3, "lat": 38.5, "lon": 27.1},
                {"type": "way", "id": 100, "nodes": [1, 2], "tags": {"highway": "primary"}},
                {"type": "way", "id": 200, "nodes": [1, 2, 3, 1], "tags": {"building": "yes"}},
            ]
        }
        res = _overpass_to_geojson(mock_osm)
        self.assertEqual(len(res["features"]), 2)
        self.assertEqual(res["features"][0]["geometry"]["type"], "LineString")
        self.assertEqual(res["features"][1]["geometry"]["type"], "Polygon")

    def test_cli(self) -> None:
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".png") as tmp_img:
            self.img.save(tmp_img.name)
            img_path = tmp_img.name

        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".svg") as tmp_out:
            out_path = tmp_out.name

        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".geojson") as tmp_json:
            json_path = tmp_json.name

        try:
            # Test presets command
            ret_presets = myface2city.cli.main(["presets"])
            self.assertEqual(ret_presets, 0)

            # Test render command
            ret_render = myface2city.cli.main(
                [
                    "render",
                    "--image",
                    img_path,
                    "--preset",
                    "Cyberpunk 2077",
                    "--output",
                    out_path,
                ]
            )
            self.assertEqual(ret_render, 0)
            self.assertTrue(os.path.exists(out_path))

            # Test render to geojson
            ret_render_json = myface2city.cli.main(
                [
                    "render",
                    "--image",
                    img_path,
                    "--output",
                    json_path,
                ]
            )
            self.assertEqual(ret_render_json, 0)

            # Test stipple command
            ret_stipple = myface2city.cli.main(
                [
                    "stipple",
                    "--image",
                    img_path,
                    "--cols",
                    "15",
                    "--rows",
                    "15",
                    "--output",
                    out_path,
                ]
            )
            self.assertEqual(ret_stipple, 0)
        finally:
            if os.path.exists(img_path):
                os.remove(img_path)
            if os.path.exists(out_path):
                os.remove(out_path)
            if os.path.exists(json_path):
                os.remove(json_path)


if __name__ == "__main__":
    unittest.main()
