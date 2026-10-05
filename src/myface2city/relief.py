# -*- coding: utf-8 -*-
"""Multi-Layer 3D Relief & Extrusion Mesh Exporter for MyFace2City."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image


@dataclass
class ReliefMesh3D:
    """Represents a 3D topographic / portrait extrusion mesh."""

    vertices: list[tuple[float, float, float]]  # (x, y, z)
    faces: list[tuple[int, int, int]]  # 1-indexed triangle vertex indices for OBJ
    normals: list[tuple[float, float, float]] = field(default_factory=list)
    uvs: list[tuple[float, float]] = field(default_factory=list)

    def to_obj(self) -> str:
        """Export as standard Wavefront .OBJ 3D file."""
        lines = [
            "# MyFace2City 3D Relief Mesh Exporter",
            f"# Vertices: {len(self.vertices)} | Faces: {len(self.faces)}",
        ]

        for x, y, z in self.vertices:
            lines.append(f"v {x:.4f} {y:.4f} {z:.4f}")

        for u, v in self.uvs:
            lines.append(f"vt {u:.4f} {v:.4f}")

        for nx, ny, nz in self.normals:
            lines.append(f"vn {nx:.4f} {ny:.4f} {nz:.4f}")

        for f1, f2, f3 in self.faces:
            if self.normals and self.uvs:
                lines.append(f"f {f1}/{f1}/{f1} {f2}/{f2}/{f2} {f3}/{f3}/{f3}")
            elif self.uvs:
                lines.append(f"f {f1}/{f1} {f2}/{f2} {f3}/{f3}")
            else:
                lines.append(f"f {f1} {f2} {f3}")

        return "\n".join(lines)

    def save_obj(self, filepath: str | Path) -> None:
        """Write mesh directly to OBJ file."""
        p = Path(filepath)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(self.to_obj(), encoding="utf-8")


def generate_3d_relief_mesh(
    image: Image.Image,
    grid_size: int = 64,
    max_height: float = 20.0,
    base_thickness: float = 2.0,
    invert_height: bool = True,
) -> ReliefMesh3D:
    """Generate a 3D extruded terrain / portrait relief surface mesh from image luminance.

    Args:
        image: PIL Image object.
        grid_size: Resolution of the square mesh grid (e.g. 64x64).
        max_height: Maximum Z height of the relief extrusion.
        base_thickness: Base substrate thickness below the lowest point.
        invert_height: If True, darker regions become taller (classic lithophane / urban density).

    Returns:
        ReliefMesh3D object with vertices, triangles, normals, and UVs.
    """
    img_gray = image.convert("L").resize((grid_size, grid_size), Image.Resampling.BILINEAR)
    pixels = img_gray.load()

    vertices: list[tuple[float, float, float]] = []
    uvs: list[tuple[float, float]] = []
    normals: list[tuple[float, float, float]] = []
    faces: list[tuple[int, int, int]] = []

    # 1. Generate top surface vertices
    for y in range(grid_size):
        for x in range(grid_size):
            lum = pixels[x, y] / 255.0
            height_factor = (1.0 - lum) if invert_height else lum
            z = base_thickness + height_factor * max_height

            vx = float(x)
            vy = float(y)
            vertices.append((vx, vy, z))
            uvs.append((x / (grid_size - 1), 1.0 - (y / (grid_size - 1))))
            normals.append((0.0, 0.0, 1.0))

    # 2. Build surface triangle faces (1-indexed for OBJ)
    for y in range(grid_size - 1):
        for x in range(grid_size - 1):
            top_left = y * grid_size + x + 1
            top_right = top_left + 1
            bottom_left = (y + 1) * grid_size + x + 1
            bottom_right = bottom_left + 1

            # Triangle 1: top_left, bottom_left, top_right
            faces.append((top_left, bottom_left, top_right))
            # Triangle 2: top_right, bottom_left, bottom_right
            faces.append((top_right, bottom_left, bottom_right))

    return ReliefMesh3D(
        vertices=vertices,
        faces=faces,
        normals=normals,
        uvs=uvs,
    )
