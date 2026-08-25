"""
Dependency-free tone transforms, coordinate normalizers, and histogram statistics.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class NormalizedPoint:
    """Image coordinates normalized to the inclusive 0.0 .. 1.0 range."""

    u: float
    v: float


def fit_bounds_to_aspect(
    bounds: tuple[float, float, float, float],
    aspect_ratio: float,
) -> tuple[float, float, float, float]:
    """Center the largest undistorted image frame inside the supplied bounding box (min_x, min_y, max_x, max_y)."""
    min_x, min_y, max_x, max_y = bounds
    width = max_x - min_x
    height = max_y - min_y
    ratio = float(aspect_ratio)

    if width <= 0.0 or height <= 0.0:
        raise ValueError("Image frame bounds must have positive width and height.")
    if ratio <= 0.0:
        raise ValueError("Image aspect ratio must be positive.")

    frame_ratio = width / height
    if frame_ratio > ratio:
        fitted_width = height * ratio
        inset = (width - fitted_width) / 2.0
        return min_x + inset, min_y, max_x - inset, max_y
    if frame_ratio < ratio:
        fitted_height = width / ratio
        inset = (height - fitted_height) / 2.0
        return min_x, min_y + inset, max_x, max_y - inset
    return bounds


def map_to_normalized(
    x: float,
    y: float,
    bounds: tuple[float, float, float, float],
) -> NormalizedPoint | None:
    """Map a world/geographic point to image coordinates (0..1), flipping vertical Y axis."""
    min_x, min_y, max_x, max_y = bounds
    width = max_x - min_x
    height = max_y - min_y

    if width <= 0.0 or height <= 0.0 or x < min_x or x > max_x or y < min_y or y > max_y:
        return None
    return NormalizedPoint((x - min_x) / width, (max_y - y) / height)


def adjust_luminance(
    value: float,
    low: float = 0.0,
    high: float = 255.0,
    gamma: float = 1.0,
    invert: bool = False,
) -> int:
    """Stretch, gamma-correct, and optionally invert an 8-bit luminance value (0..255)."""
    if high <= low:
        high = low + 1.0
    normalized = min(1.0, max(0.0, (float(value) - low) / (high - low)))
    corrected = math.pow(normalized, 1.0 / max(0.05, float(gamma)))
    if invert:
        corrected = 1.0 - corrected
    return int(round(corrected * 255.0))


def quantile_limits(histogram: list[int], clip_fraction: float = 0.01) -> tuple[int, int]:
    """Return robust low/high histogram limits for automatic image contrast stretching."""
    total = sum(max(0, int(count)) for count in histogram[:256])
    if total <= 0:
        return 0, 255
    target = total * min(0.25, max(0.0, clip_fraction))
    running = 0
    low = 0
    for idx, count in enumerate(histogram[:256]):
        running += max(0, int(count))
        if running >= target:
            low = idx
            break
    running = 0
    high = 255
    for idx in range(min(255, len(histogram) - 1), -1, -1):
        running += max(0, int(histogram[idx]))
        if running >= target:
            high = idx
            break
    return (low, high) if high > low else (0, 255)


def blend_edge(luminance: int, edge_strength: int, amount: float) -> int:
    """Darken image edges while preserving the underlying tonal portrait luminance."""
    mix = min(1.0, max(0.0, float(amount)))
    edge_tone = 255 - min(255, max(0, int(edge_strength)))
    return int(round((1.0 - mix) * luminance + mix * min(luminance, edge_tone)))
