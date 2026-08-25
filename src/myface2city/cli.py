"""
Command-line interface for MyFace2City.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image

from .engine import RenderConfig, UrbanPortrait
from .export import export_svg
from .osm import fetch_osm_network, generate_synthetic_urban_grid
from .presets import PRESETS
from .stipple import calculate_stipple_points, stipple_to_geojson


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="myface2city",
        description="Turn urban street networks, building footprints, and vector maps into live optical portrait art.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 1. Presets command
    subparsers.add_parser("presets", help="List all available art presets and colorways.")

    # 2. Render command
    render_parser = subparsers.add_parser("render", help="Render an image onto a vector network or OSM bounding box.")
    render_parser.add_argument("--image", required=True, help="Path to input portrait/face image.")
    render_parser.add_argument("--vector", help="Path to input GeoJSON vector network (roads, buildings, etc.).")
    render_parser.add_argument("--osm-bbox", help="Bounding box to fetch OSM data (min_lon,min_lat,max_lon,max_lat).")
    render_parser.add_argument(
        "--preset", default="Ink Portrait", help="Art preset name (e.g., 'Cyberpunk 2077', 'Blueprint')."
    )
    render_parser.add_argument("--gamma", type=float, default=1.0, help="Gamma correction factor.")
    render_parser.add_argument("--invert", action="store_true", help="Invert image tones (negative mode).")
    render_parser.add_argument("--output", "-o", default="artwork.svg", help="Output file path (.svg or .geojson).")

    # 3. Stipple command
    stipple_parser = subparsers.add_parser(
        "stipple", help="Generate algorithmic halftone / engraving vector stippling dots."
    )
    stipple_parser.add_argument("--image", required=True, help="Path to input portrait image.")
    stipple_parser.add_argument("--cols", type=int, default=80, help="Number of horizontal grid columns.")
    stipple_parser.add_argument("--rows", type=int, default=80, help="Number of vertical grid rows.")
    stipple_parser.add_argument("--max-radius", type=float, default=4.0, help="Maximum dot radius.")
    stipple_parser.add_argument("--preset", default="Ink Portrait", help="Art preset name.")
    stipple_parser.add_argument("--output", "-o", default="stipple.svg", help="Output file path (.svg or .geojson).")

    args = parser.parse_args(argv)

    if args.command == "presets":
        print("\n🎨 MyFace2City Curated Art Presets:")
        print("=" * 60)
        for name, p in PRESETS.items():
            print(f"• {name:<18} | BG: {p.background} | Colors: {' '.join(p.colors)}")
        print("=" * 60)
        return 0

    if args.command == "render":
        img_path = Path(args.image)
        if not img_path.exists():
            print(f"Error: Image not found: {img_path}", file=sys.stderr)
            return 1

        img = Image.open(str(img_path))

        # Vector network source
        if args.vector:
            v_path = Path(args.vector)
            if not v_path.exists():
                print(f"Error: Vector file not found: {v_path}", file=sys.stderr)
                return 1
            geojson_data = json.loads(v_path.read_text(encoding="utf-8"))
            bounds = (0.0, 0.0, 100.0, 100.0)
        elif args.osm_bbox:
            bbox_parts = [float(x) for x in args.osm_bbox.split(",")]
            bbox = (bbox_parts[0], bbox_parts[1], bbox_parts[2], bbox_parts[3])
            print(f"Fetching OpenStreetMap data for bbox {bbox}...")
            try:
                geojson_data = fetch_osm_network(bbox)
            except Exception as e:
                print(
                    f"Warning: OSM download failed ({e}), generating synthetic city grid for preview.", file=sys.stderr
                )
                geojson_data = generate_synthetic_urban_grid(bbox)
            bounds = bbox
        else:
            print("Notice: No vector or OSM bbox provided. Generating synthetic urban street network for preview.")
            bounds = (27.10, 38.40, 27.15, 38.45)
            geojson_data = generate_synthetic_urban_grid(bounds)

        cfg = RenderConfig(preset=args.preset, gamma=args.gamma, invert=args.invert)
        portrait = UrbanPortrait(img, bounds, cfg)
        styled_geojson = portrait.process_geojson(geojson_data, args.preset)

        out_path = Path(args.output)
        if out_path.suffix.lower() == ".geojson":
            out_path.write_text(json.dumps(styled_geojson, indent=2, ensure_ascii=False), encoding="utf-8")
        else:
            export_svg(styled_geojson, out_path, preset=args.preset)

        print(f"✨ Artwork rendered successfully to: {out_path}")
        return 0

    if args.command == "stipple":
        img_path = Path(args.image)
        if not img_path.exists():
            print(f"Error: Image not found: {img_path}", file=sys.stderr)
            return 1

        img = Image.open(str(img_path)).convert("L")
        w, h = img.size
        pixels = img.load()

        def sample_fn(u: float, v: float) -> float:
            px = int(max(0.0, min(1.0, u)) * (w - 1))
            py = int(max(0.0, min(1.0, v)) * (h - 1))
            return float(pixels[px, py])

        points = calculate_stipple_points(
            0.0,
            0.0,
            100.0,
            100.0,
            grid_cols=args.cols,
            grid_rows=args.rows,
            sample_fn=sample_fn,
            max_radius=args.max_radius,
            preset=args.preset,
        )

        stipple_geojson = stipple_to_geojson(points)
        out_path = Path(args.output)

        if out_path.suffix.lower() == ".geojson":
            out_path.write_text(json.dumps(stipple_geojson, indent=2, ensure_ascii=False), encoding="utf-8")
        else:
            export_svg(stipple_geojson, out_path, preset=args.preset)

        print(f"✨ Halftone stippling artwork ({len(points)} dots) generated: {out_path}")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
