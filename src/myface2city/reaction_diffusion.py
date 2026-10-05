# -*- coding: utf-8 -*-
"""Reaction-Diffusion (Gray-Scott PDE) Turing Pattern Portrait Synthesizer for myface2city."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image


@dataclass
class TuringPatternArtwork:
    """Organic reaction-diffusion Turing pattern artwork."""

    width: int
    height: int
    chemical_b_matrix: list[list[float]]

    def to_image(self, foreground_color: tuple[int, int, int] = (255, 255, 255), background_color: tuple[int, int, int] = (15, 23, 42)) -> Image.Image:
        img = Image.new("RGB", (self.width, self.height), background_color)
        pixels = img.load()
        for r in range(self.height):
            for c in range(self.width):
                b = self.chemical_b_matrix[r][c]
                t = max(0.0, min(1.0, b * 2.5))
                red = int(background_color[0] * (1 - t) + foreground_color[0] * t)
                green = int(background_color[1] * (1 - t) + foreground_color[1] * t)
                blue = int(background_color[2] * (1 - t) + foreground_color[2] * t)
                pixels[c, r] = (red, green, blue)
        return img


def simulate_gray_scott(
    width: int,
    height: int,
    feed_matrix: list[list[float]],
    kill_matrix: list[list[float]],
    iterations: int = 25,
    da: float = 1.0,
    db: float = 0.5,
    dt: float = 1.0,
) -> list[list[float]]:
    """Solve 2D discrete Laplacian Gray-Scott reaction-diffusion PDE:

    dA/dt = D_A * \nabla^2 A - A*B^2 + F*(1 - A)
    dB/dt = D_B * \nabla^2 B + A*B^2 - (F + k)*B
    """
    # Initialize grids (A=1.0, B=0.0 with center seed)
    grid_a = [[1.0] * width for _ in range(height)]
    grid_b = [[0.0] * width for _ in range(height)]

    # Seed central square
    cx, cy = width // 2, height // 2
    r_seed = max(2, min(width, height) // 6)
    for r in range(cy - r_seed, cy + r_seed):
        for c in range(cx - r_seed, cx + r_seed):
            if 0 <= r < height and 0 <= c < width:
                grid_b[r][c] = 1.0

    for _ in range(iterations):
        next_a = [[1.0] * width for _ in range(height)]
        next_b = [[0.0] * width for _ in range(height)]

        for r in range(height):
            r_prev = (r - 1) % height
            r_next = (r + 1) % height
            for c in range(width):
                c_prev = (c - 1) % width
                c_next = (c + 1) % width

                a = grid_a[r][c]
                b = grid_b[r][c]

                # 5-point discrete Laplacian stencil
                lap_a = (grid_a[r_prev][c] + grid_a[r_next][c] + grid_a[r][c_prev] + grid_a[r][c_next]) * 0.25 - a
                lap_b = (grid_b[r_prev][c] + grid_b[r_next][c] + grid_b[r][c_prev] + grid_b[r][c_next]) * 0.25 - b

                f = feed_matrix[r][c]
                k = kill_matrix[r][c]

                reaction = a * b * b
                next_a[r][c] = a + (da * lap_a - reaction + f * (1.0 - a)) * dt
                next_b[r][c] = b + (db * lap_b + reaction - (f + k) * b) * dt

                # Clamp
                next_a[r][c] = max(0.0, min(1.0, next_a[r][c]))
                next_b[r][c] = max(0.0, min(1.0, next_b[r][c]))

        grid_a = next_a
        grid_b = next_b

    return grid_b


def generate_turing_portrait(
    image: Image.Image | str | Path,
    resolution: int = 48,
    iterations: int = 30,
) -> TuringPatternArtwork:
    """Modulate reaction-diffusion feed & kill fields with portrait image luminance."""
    if not isinstance(image, Image.Image):
        img = Image.open(image).convert("L")
    else:
        img = image.convert("L")

    small = img.resize((resolution, resolution), Image.Resampling.LANCZOS)
    pixels = small.load()

    feed_mat: list[list[float]] = []
    kill_mat: list[list[float]] = []

    for r in range(resolution):
        f_row = []
        k_row = []
        for c in range(resolution):
            lum = pixels[c, r] / 255.0  # 0 to 1
            # Feed ranges from 0.030 to 0.065
            f_val = 0.030 + lum * 0.035
            # Kill ranges from 0.055 to 0.065
            k_val = 0.055 + (1.0 - lum) * 0.010
            f_row.append(f_val)
            k_row.append(k_val)
        feed_mat.append(f_row)
        kill_mat.append(k_row)

    b_mat = simulate_gray_scott(resolution, resolution, feed_mat, kill_mat, iterations=iterations)
    return TuringPatternArtwork(width=resolution, height=resolution, chemical_b_matrix=b_mat)
