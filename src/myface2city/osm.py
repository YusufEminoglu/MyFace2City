"""
OpenStreetMap Data Acquisition Engine:
Fetches road networks, building footprints, and water bodies from Overpass API into GeoJSON.
"""

from __future__ import annotations

import json
import math
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

OVERPASS_SERVERS = [
    "https://overpass-api.de/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
]


def fetch_osm_network(
    bbox: tuple[float, float, float, float],
    network_type: str = "all",  # "roads", "buildings", "all"
    timeout: int = 25,
) -> dict[str, Any]:
    """Fetch OpenStreetMap vector features for a bounding box (min_lon, min_lat, max_lon, max_lat)."""
    min_lon, min_lat, max_lon, max_lat = bbox

    # Safety check: Prevent excessive global queries (> 25 sq km)
    dx_km = (max_lon - min_lon) * 111.0 * math.cos(math.radians((min_lat + max_lat) / 2.0))
    dy_km = (max_lat - min_lat) * 111.0
    area_sqkm = abs(dx_km * dy_km)

    if area_sqkm > 100.0:
        raise ValueError(
            f"Requested bounding box is too large ({area_sqkm:.1f} km² > 100 km²). Please select a neighborhood or city scale."
        )

    query_parts = []
    if network_type in ("roads", "all"):
        query_parts.append(f'way["highway"]({min_lat},{min_lon},{max_lat},{max_lon});')
    if network_type in ("buildings", "all"):
        query_parts.append(f'way["building"]({min_lat},{min_lon},{max_lat},{max_lon});')
        query_parts.append(f'relation["building"]({min_lat},{min_lon},{max_lat},{max_lon});')

    query_str = f"""
    [out:json][timeout:{timeout}];
    (
        {" ".join(query_parts)}
    );
    out body;
    >;
    out skel qt;
    """

    encoded = urllib.parse.urlencode({"data": query_str}).encode("utf-8")
    last_err = None

    for server in OVERPASS_SERVERS:
        try:
            req = urllib.request.Request(server, data=encoded, headers={"User-Agent": "MyFace2City/0.1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw_json = json.loads(resp.read().decode("utf-8"))
                return _overpass_to_geojson(raw_json)
        except Exception as e:
            last_err = e
            continue

    # If offline or failed, raise helpful error
    raise ConnectionError(f"Failed to query OpenStreetMap Overpass servers: {last_err}")


def _overpass_to_geojson(osm_json: dict[str, Any]) -> dict[str, Any]:
    """Convert raw Overpass JSON elements to a GeoJSON FeatureCollection."""
    nodes: dict[int, tuple[float, float]] = {}
    ways: list[dict[str, Any]] = []

    for elem in osm_json.get("elements", []):
        e_type = elem.get("type")
        if e_type == "node":
            nodes[elem["id"]] = (elem["lon"], elem["lat"])
        elif e_type == "way":
            ways.append(elem)

    features = []
    for way in ways:
        node_ids = way.get("nodes", [])
        coords = [nodes[nid] for nid in node_ids if nid in nodes]
        if len(coords) < 2:
            continue

        tags = way.get("tags", {})
        is_building = "building" in tags
        is_closed = coords[0] == coords[-1]

        if is_building and is_closed and len(coords) >= 4:
            geom = {"type": "Polygon", "coordinates": [coords]}
        else:
            geom = {"type": "LineString", "coordinates": coords}

        features.append(
            {
                "type": "Feature",
                "id": way["id"],
                "geometry": geom,
                "properties": tags,
            }
        )

    return {"type": "FeatureCollection", "features": features}


def generate_synthetic_urban_grid(
    bbox: tuple[float, float, float, float] = (27.10, 38.40, 27.15, 38.45),
    grid_density: int = 15,
) -> dict[str, Any]:
    """Generate a synthetic urban road grid and building parcels for testing and offline art creation."""
    min_x, min_y, max_x, max_y = bbox
    dx = (max_x - min_x) / grid_density
    dy = (max_y - min_y) / grid_density

    features = []

    # Horizontal roads
    for i in range(grid_density + 1):
        y = min_y + i * dy
        features.append(
            {
                "type": "Feature",
                "geometry": {"type": "LineString", "coordinates": [[min_x, y], [max_x, y]]},
                "properties": {"highway": "residential", "name": f"Avenue {i + 1}"},
            }
        )

    # Vertical roads
    for j in range(grid_density + 1):
        x = min_x + j * dx
        features.append(
            {
                "type": "Feature",
                "geometry": {"type": "LineString", "coordinates": [[x, min_y], [x, max_y]]},
                "properties": {"highway": "secondary", "name": f"Street {j + 1}"},
            }
        )

    # Blocks / Parcels inside cells
    for i in range(grid_density):
        for j in range(grid_density):
            cx = min_x + (j + 0.2) * dx
            cy = min_y + (i + 0.2) * dy
            w = dx * 0.6
            h = dy * 0.6
            features.append(
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [cx, cy],
                                [cx + w, cy],
                                [cx + w, cy + h],
                                [cx, cy + h],
                                [cx, cy],
                            ]
                        ],
                    },
                    "properties": {"building": "yes", "parcel_id": f"{i}_{j}"},
                }
            )

    return {"type": "FeatureCollection", "features": features}
