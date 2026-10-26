# -*- coding: utf-8 -*-
"""Typed Pillow pixel helpers shared by the myface2city art engines."""

from __future__ import annotations

from typing import Any, cast

from PIL import Image


def load_pixels(img: Image.Image) -> Any:
    """Return the pixel accessor of ``img``, failing loudly if Pillow cannot provide one.

    Pillow types pixel values as a union over every image mode. The engines only read
    ``"L"`` (int) or ``"RGB"`` (3-tuple) images, so the accessor is returned untyped and
    each caller relies on the mode it converted to.
    """
    pixels = img.load()
    if pixels is None:
        raise ValueError(f"Image in mode {img.mode!r} has no pixel data")
    return pixels


def gray_at(img: Image.Image, xy: tuple[int, int]) -> int:
    """Return the 8-bit luminance of an ``"L"`` mode image at ``xy``."""
    return cast(int, img.getpixel(xy))


def rgb_at(img: Image.Image, xy: tuple[int, int]) -> tuple[int, int, int]:
    """Return the ``(r, g, b)`` triple of an ``"RGB"`` mode image at ``xy``."""
    return cast("tuple[int, int, int]", img.getpixel(xy))
