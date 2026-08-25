# -*- coding: utf-8 -*-
"""
Art-direction presets, colorways, and palette management for MyFace2City.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

_COLOR_PATTERN = re.compile(r"^#[0-9a-fA-F]{6}(?:[0-9a-fA-F]{2})?$")
TONE_BREAKS = (0, 52, 104, 156, 208, 256)


@dataclass(frozen=True)
class Palette:
    """A 5-tone colorway and styling configuration."""

    name: str
    colors: tuple[str, str, str, str, str]  # Deep Shadow, Dark, Midtone, Light, Highlight
    background: str
    widths: tuple[float, float, float, float, float]
    hide_highlights: bool = False

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "colors": list(self.colors),
            "background": self.background,
            "widths": list(self.widths),
            "hide_highlights": self.hide_highlights,
        }

    @classmethod
    def from_dict(cls, data: dict, name: str = "Custom") -> "Palette":
        colors = tuple(str(c) for c in data.get("colors", ["#000000"] * 5))
        widths = tuple(float(w) for w in data.get("widths", [1.0, 0.8, 0.6, 0.4, 0.2]))
        bg = str(data.get("background", "#ffffff"))
        hide = bool(data.get("hide_highlights", False))
        return cls(
            name=str(data.get("name", name)),
            colors=colors[:5],
            background=bg,
            widths=widths[:5],
            hide_highlights=hide,
        )


PRESETS: dict[str, Palette] = {
    "Ink Portrait": Palette(
        name="Ink Portrait",
        colors=("#090b10", "#20242d", "#4d535f", "#a8adb5", "#e7e9ec"),
        background="#f5f1e8",
        widths=(1.35, 1.0, 0.68, 0.38, 0.12),
        hide_highlights=True,
    ),
    "Neon Night": Palette(
        name="Neon Night",
        colors=("#ff477e", "#7b2cff", "#00c2ff", "#5eead4", "#c8fff4"),
        background="#050816",
        widths=(1.55, 1.15, 0.78, 0.42, 0.14),
        hide_highlights=False,
    ),
    "Blueprint": Palette(
        name="Blueprint",
        colors=("#effcff", "#a7e8f2", "#58c9da", "#2389a1", "#155064"),
        background="#082f49",
        widths=(1.3, 0.95, 0.65, 0.36, 0.12),
        hide_highlights=False,
    ),
    "Sepia Blocks": Palette(
        name="Sepia Blocks",
        colors=("#2c1810", "#5b3424", "#8f5f3e", "#c69b6d", "#ead7b7"),
        background="#f1e3c6",
        widths=(1.4, 1.05, 0.7, 0.4, 0.12),
        hide_highlights=True,
    ),
    "Negative City": Palette(
        name="Negative City",
        colors=("#f7f7ff", "#c7d2fe", "#818cf8", "#4338ca", "#111133"),
        background="#07071a",
        widths=(1.45, 1.08, 0.72, 0.4, 0.12),
        hide_highlights=False,
    ),
    "Cyberpunk 2077": Palette(
        name="Cyberpunk 2077",
        colors=("#060814", "#7000ff", "#ff0055", "#00f0ff", "#ffe600"),
        background="#050811",
        widths=(1.50, 1.10, 0.75, 0.40, 0.14),
        hide_highlights=False,
    ),
    "Vintage Engraving": Palette(
        name="Vintage Engraving",
        colors=("#2c1d11", "#4a3525", "#70533d", "#a48366", "#d8c5b0"),
        background="#f6eee3",
        widths=(1.35, 1.00, 0.68, 0.38, 0.12),
        hide_highlights=True,
    ),
    "Thermal Heatmap": Palette(
        name="Thermal Heatmap",
        colors=("#0a0826", "#4d006e", "#a8184c", "#f36410", "#f9f871"),
        background="#050414",
        widths=(1.50, 1.12, 0.74, 0.38, 0.13),
        hide_highlights=False,
    ),
    "Emerald Eco-Map": Palette(
        name="Emerald Eco-Map",
        colors=("#061c14", "#0f3d2e", "#1e6b52", "#3fa882", "#7be3bc"),
        background="#030f0b",
        widths=(1.40, 1.05, 0.70, 0.38, 0.12),
        hide_highlights=False,
    ),
    "Nordic Slate": Palette(
        name="Nordic Slate",
        colors=("#12171c", "#242d38", "#414f5e", "#7a8a9e", "#cbd5e1"),
        background="#f1f5f9",
        widths=(1.30, 0.95, 0.65, 0.35, 0.12),
        hide_highlights=True,
    ),
}


def get_preset(name: str) -> Palette:
    """Retrieve an art preset by exact or case-insensitive name."""
    if name in PRESETS:
        return PRESETS[name]
    low = name.lower().replace(" ", "").replace("_", "").replace("-", "")
    for k, v in PRESETS.items():
        if k.lower().replace(" ", "").replace("_", "").replace("-", "") == low:
            return v
    # Fallback to Ink Portrait
    return PRESETS["Ink Portrait"]


def list_presets() -> list[str]:
    """Return all available preset names."""
    return list(PRESETS.keys())


def load_custom_palette(file_path: str | Path) -> Palette:
    """Load a custom palette from a JSON file."""
    path = Path(file_path)
    data = json.loads(path.read_text(encoding="utf-8"))
    return Palette.from_dict(data, name=path.stem)


def save_custom_palette(palette: Palette, file_path: str | Path) -> None:
    """Save a palette to a JSON file."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(palette.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
