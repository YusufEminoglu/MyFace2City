# -*- coding: utf-8 -*-
"""myface2city Cookbook — Flow Fields, CMYK Plates & ASCII Typographic Art."""

import myface2city
from PIL import Image

test_img = Image.new("RGB", (64, 64), color="lightblue")

# 1. Flow-Field Vector Streamlines
flow_art = myface2city.generate_flow_field_art(test_img, num_particles=100)
svg = flow_art.to_svg()
print(f"Flow-Field SVG lines: {len(flow_art.streamlines)}")

# 2. CMYK Separation Plates
cmyk = myface2city.generate_cmyk_screen_layers(test_img, grid_cells_x=20)
print(f"Separation Plates: {[p.plate_name for p in cmyk.plates]}")

# 3. Typographic ASCII Map Art
ascii_art = myface2city.generate_ascii_map_art(test_img, cols=30)
print(f"Typographic rows: {ascii_art.rows}")
