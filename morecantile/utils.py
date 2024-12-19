"""morecantile utils."""

import math
from typing import Dict, List

from pyproj import CRS
from pyproj.enums import WktVersion

from morecantile.commons import BoundingBox, Coords, Tile
from morecantile.errors import TileArgParsingError


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


def lons_contain_antimeridian(lon1: float, lon2: float) -> bool:
    """
    Check if the antimeridian (180th meridian) is between two longitude points

    Parameters
    ----------
    lon1: float
        The first longitude.
    lon2: float
        The second longitude

    Returns
    -------
    A bool representing whether two longs contain the 180th meridian.
    """
    lon1_clipped = max(-180.0, min(lon1, 180))
    lon2_clipped = max(-180.0, min(lon2, 180))
    lon1_converted = (lon1_clipped + 360) % 360
    lon2_converted = (lon2_clipped + 360) % 360
    ws = [lon1_converted, lon2_converted]
    sorted(ws)
    return ws[0] < 180 < ws[1]


def meters_per_unit(crs: CRS) -> float:
    """
    Coefficient to convert the coordinate reference system (CRS)
    units into meters (metersPerUnit).

    From note g in http://docs.opengeospatial.org/is/17-083r2/17-083r2.html#table_2:
        If the CRS uses meters as units of measure for the horizontal dimensions,
        then metersPerUnit=1; if it has degrees, then metersPerUnit=2pa/360
        (a is the Earth maximum radius of the ellipsoid).

    """
    unit_factors = {
        "metre": 1.0,
        "degree": 2 * math.pi * crs.ellipsoid.semi_major_metre / 360.0,
        "foot": 0.3048,
        "US survey foot": 0.30480060960121924,
    }
    unit_name = crs.axis_info[0].unit_name
    try:
        return unit_factors[unit_name]
    except KeyError as e:
        raise Exception(
            f"CRS {crs} with Unit Name `{unit_name}` is not supported, please fill an issue in developmentseed/morecantile"
        ) from e


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


def is_power_of_two(number: int) -> bool:
    """Check if a number is a power of 2"""
    return (number & (number - 1) == 0) and number != 0


def check_quadkey_support(tms: List) -> bool:
    """Check if a Tile Matrix Set supports quadkeys"""
    return all(
        (t.matrixWidth == t.matrixHeight)
        and is_power_of_two(t.matrixWidth)
        and ((t.matrixWidth * 2) == tms[i + 1].matrixWidth)
        for i, t in enumerate(tms[:-1])
    )


def to_rasterio_crs(incrs: CRS):
    """Convert a pyproj CRS to a rasterio CRS"""
    from rasterio import crs
    from rasterio.env import GDALVersion

    if GDALVersion.runtime().major < 3:
        return crs.CRS.from_wkt(incrs.to_wkt(WktVersion.WKT1_GDAL))
    else:
        return crs.CRS.from_wkt(incrs.to_wkt())
