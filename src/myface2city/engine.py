"""
UrbanPortrait Core Engine:
Binds portrait imagery to geographic networks and styles vector features by luminance.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Union

from PIL import Image

from .presets import Palette, get_preset
from .profile import (
    adjust_luminance,
    fit_bounds_to_aspect,
    map_to_normalized,
    quantile_limits,
)


@dataclass
class RenderConfig:
    """Configuration for portrait sampling and tone processing."""

    preset: str = "Ink Portrait"
    sampling: str = "balanced"  # center, balanced, high_quality
    gamma: float = 1.0
    invert: bool = False
    auto_contrast: bool = True
    clip_fraction: float = 0.01
    edge_amount: float = 0.0
    max_features: int = 50000
    opacity: float = 1.0


class UrbanPortrait:
    """Map-locked optical portrait engine driving vector styling from raster luminance."""

    def __init__(
        self,
        image_source: Union[str, Path, Image.Image],
        bounds: tuple[float, float, float, float],
        config: RenderConfig | None = None,
    ) -> None:
        self.config = config or RenderConfig()

        # Load image via PIL
        if isinstance(image_source, (str, Path)):
            self.image = Image.open(str(image_source)).convert("L")
        elif isinstance(image_source, Image.Image):
            self.image = image_source.convert("L")
        else:
            raise TypeError(f"Unsupported image_source type: {type(image_source)}")

        self.img_width, self.img_height = self.image.size
        self.aspect_ratio = self.img_width / max(1, self.img_height)

        # Fit geographic bounds to image aspect ratio
        self.raw_bounds = bounds
        self.fitted_bounds = fit_bounds_to_aspect(bounds, self.aspect_ratio)

        # Precompute histogram and auto-contrast limits
        self.histogram = self.image.histogram()
        if self.config.auto_contrast:
            self.low_limit, self.high_limit = quantile_limits(self.histogram, self.config.clip_fraction)
        else:
            self.low_limit, self.high_limit = 0, 255

        # Cache pixel lookup
        self._pixels = self.image.load()

    def sample_pixel(self, u: float, v: float) -> int:
        """Sample raw 8-bit luminance at normalized coordinate (0..1, 0..1)."""
        u = max(0.0, min(1.0, float(u)))
        v = max(0.0, min(1.0, float(v)))
        px = int(u * (self.img_width - 1))
        py = int(v * (self.img_height - 1))
        return int(self._pixels[px, py])

    def sample_point(self, x: float, y: float) -> int | None:
        """Sample tone-adjusted luminance at a world/geographic coordinate (x, y)."""
        norm_pt = map_to_normalized(x, y, self.fitted_bounds)
        if norm_pt is None:
            return None

        raw_luma = self.sample_pixel(norm_pt.u, norm_pt.v)
        adjusted = adjust_luminance(
            raw_luma,
            low=self.low_limit,
            high=self.high_limit,
            gamma=self.config.gamma,
            invert=self.config.invert,
        )
        return adjusted

    def sample_geometry(self, geometry: dict[str, Any]) -> int:
        """Sample average luminance across points, linestrings, or polygons."""
        g_type = geometry.get("type", "")
        coords = geometry.get("coordinates", [])

        if g_type == "Point" and coords:
            luma = self.sample_point(coords[0], coords[1])
            return luma if luma is not None else 255

        if g_type in ("LineString", "MultiPoint") and coords:
            samples = []
            if self.config.sampling == "center" or len(coords) < 3:
                # Sample middle vertex
                mid_idx = len(coords) // 2
                lum = self.sample_point(coords[mid_idx][0], coords[mid_idx][1])
                if lum is not None:
                    samples.append(lum)
            elif self.config.sampling == "balanced":
                # Sample start, middle, end
                for idx in [0, len(coords) // 2, -1]:
                    lum = self.sample_point(coords[idx][0], coords[idx][1])
                    if lum is not None:
                        samples.append(lum)
            else:  # high_quality
                for pt in coords:
                    lum = self.sample_point(pt[0], pt[1])
                    if lum is not None:
                        samples.append(lum)

            return int(round(sum(samples) / len(samples))) if samples else 255

        if g_type in ("Polygon", "MultiLineString") and coords:
            ring = coords[0] if g_type == "Polygon" else coords
            samples = []
            for pt in ring[:10]:
                if isinstance(pt, (list, tuple)) and len(pt) >= 2:
                    lum = self.sample_point(pt[0], pt[1])
                    if lum is not None:
                        samples.append(lum)
            return int(round(sum(samples) / len(samples))) if samples else 255

        return 255

    def style_feature(
        self,
        feature: dict[str, Any],
        palette: str | Palette | None = None,
    ) -> dict[str, Any]:
        """Attach optical portrait styling properties to a GeoJSON feature."""
        pal = get_preset(palette or self.config.preset) if isinstance(palette, str) or palette is None else palette
        geom = feature.get("geometry", {})
        luma = self.sample_geometry(geom)

        tone_bin = min(4, int(luma / 52))
        color = pal.colors[tone_bin]
        stroke_width = pal.widths[tone_bin]
        is_hidden = pal.hide_highlights and tone_bin == 4

        props = dict(feature.get("properties", {}))
        props["_portrait_luminance"] = luma
        props["_portrait_tone"] = tone_bin
        props["_portrait_color"] = color
        props["_stroke_width"] = 0.0 if is_hidden else stroke_width
        props["_opacity"] = 0.0 if is_hidden else self.config.opacity
        props["_is_hidden"] = is_hidden

        return {
            "type": "Feature",
            "geometry": geom,
            "properties": props,
        }

    def process_geojson(
        self,
        geojson_data: dict[str, Any],
        palette: str | Palette | None = None,
    ) -> dict[str, Any]:
        """Process an entire GeoJSON FeatureCollection with optical portrait styles."""
        pal = get_preset(palette or self.config.preset) if isinstance(palette, str) or palette is None else palette
        features = geojson_data.get("features", [])
        styled_features = []

        for feat in features[: self.config.max_features]:
            styled_features.append(self.style_feature(feat, pal))

        return {
            "type": "FeatureCollection",
            "properties": {
                "preset": pal.name,
                "background": pal.background,
                "fitted_bounds": list(self.fitted_bounds),
            },
            "features": styled_features,
        }
