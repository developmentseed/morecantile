"""morecantile utils."""

import math
from typing import Dict, Tuple

from rasterio.crs import CRS

from .commons import BoundingBox, Coords, Tile
from .errors import TileArgParsingError


def _parse_tile_arg(*args) -> Tile:
    """
    Parse the *tile arg of module functions

    Copy from https://github.com/mapbox/mercantile/blob/master/mercantile/__init__.py

    Parameters
    ----------
    tile : Tile or sequence of int
        May be be either an instance of Tile or 3 ints, X, Y, Z.

    Returns
    -------
    Tile

    Raises
    ------
    TileArgParsingError

    """
    if len(args) == 1:
        args = args[0]
    if len(args) == 3:
        return Tile(*args)
    else:
        raise TileArgParsingError(
            "the tile argument may have 1 or 3 values. Note that zoom is a keyword-only argument"
        )


def meters_per_unit(crs: CRS) -> float:
    """
    Coefficient to convert the coordinate reference system (CRS)
    units into meters (metersPerUnit).

    From note g in http://docs.opengeospatial.org/is/17-083r2/17-083r2.html#table_2:
        If the CRS uses meters as units of measure for the horizontal dimensions,
        then metersPerUnit=1; if it has degrees, then metersPerUnit=2pa/360
        (a is the Earth maximum radius of the ellipsoid).

    """
    # crs.linear_units_factor[1]  GDAL 3.0
    return 1.0 if crs.linear_units == "metre" else 2 * math.pi * 6378137 / 360.0


def truncate_lnglat(lng: float, lat: float) -> Tuple[float, float]:
    """
    Truncate Lat Lon Geographic coordinates.

    Copy from https://github.com/mapbox/mercantile/blob/master/mercantile/__init__.py

    """
    if lng > 180.0:
        lng = 180.0
    elif lng < -180.0:
        lng = -180.0

    if lat > 90.0:
        lat = 90.0
    elif lat < -90.0:
        lat = -90.0

    return lng, lat


def bbox_to_feature(west: float, south: float, east: float, north: float) -> Dict:
    """Create a GeoJSON feature from a bbox."""
    return {
        "type": "Polygon",
        "coordinates": [
            [[west, south], [west, north], [east, north], [east, south], [west, south]]
        ],
    }


def point_in_bbox(point: Coords, bbox: BoundingBox, precision: int = 5) -> bool:
    """Check if a point is in a bounding box."""
    return (
        round(point.x, precision) >= round(bbox.left, precision)
        and round(point.x, precision) <= round(bbox.right, precision)
        and round(point.y, precision) >= round(bbox.bottom, precision)
        and round(point.y, precision) <= round(bbox.top, precision)
    )
