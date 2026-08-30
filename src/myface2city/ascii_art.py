# -*- coding: utf-8 -*-
"""Typographic & Character-Density Portrait Art Generator for myface2city."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Sequence
from PIL import Image


@dataclass
class ASCIIArtwork:
    """Typographic portrait text grid."""

    cols: int
    rows: int
    text_lines: list[str]
    char_palette: str

    def to_plain_text(self) -> str:
        return "\n".join(self.text_lines)

    def to_html(self, background: str = "#0f172a", text_color: str = "#38bdf8", font_size_px: int = 10) -> str:
        escaped_lines = [
            line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(" ", "&nbsp;")
            for line in self.text_lines
        ]
        body = "<br>\n".join(escaped_lines)
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Typographic Portrait Map</title>
  <style>
    body {{ background: {background}; color: {text_color}; font-family: 'Courier New', Courier, monospace; font-size: {font_size_px}px; line-height: {font_size_px}px; letter-spacing: 1px; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; padding: 20px; box-sizing: border-box; }}
    pre {{ font-weight: bold; text-shadow: 0 0 5px rgba(56, 189, 248, 0.4); }}
  </style>
</head>
<body>
  <pre>{body}</pre>
</body>
</html>"""

    def save_html(self, output_path: str | Path) -> Path:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(self.to_html(), encoding="utf-8")
        return out


def generate_ascii_map_art(
    image: Image.Image | str | Path,
    cols: int = 80,
    char_palette: str = " .:-=+*#%@",
    invert_luminance: bool = False,
) -> ASCIIArtwork:
    """Convert portrait image luminance into typographic character density artwork."""
    if not isinstance(image, Image.Image):
        img = Image.open(image).convert("L")
    else:
        img = image.convert("L")

    w, h = img.size
    # Character aspect ratio is roughly 0.55 (width/height)
    aspect = (h / max(1, w)) * 0.55
    rows = max(1, int(cols * aspect))

    small_img = img.resize((cols, rows), Image.Resampling.LANCZOS)
    pixels = small_img.load()

    palette = char_palette[::-1] if invert_luminance else char_palette
    n_chars = len(palette)

    lines: list[str] = []
    for r in range(rows):
        line_chars = []
        for c in range(cols):
            val = pixels[c, r]  # 0 to 255
            idx = int((val / 255.0) * (n_chars - 1))
            idx = max(0, min(n_chars - 1, idx))
            line_chars.append(palette[idx])
        lines.append("".join(line_chars))

    return ASCIIArtwork(
        cols=cols,
        rows=rows,
        text_lines=lines,
        char_palette=char_palette,
    )
