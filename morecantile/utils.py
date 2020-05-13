"""morecantile utils."""

import math

from rasterio.crs import CRS

from .commons import Tile
from .errors import TileArgParsingError


def _parse_tile_arg(*args) -> Tile:
    """
    parse the *tile arg of module functions

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
    coefficient to convert the coordinate reference system (CRS)
    units into meters (metersPerUnit).

    From note g in http://docs.opengeospatial.org/is/17-083r2/17-083r2.html#table_2:
        If the CRS uses meters as units of measure for the horizontal dimensions,
        then metersPerUnit=1; if it has degrees, then metersPerUnit=2pa/360
        (a is the Earth maximum radius of the ellipsoid).

    """
    # crs.linear_units_factor[1]  GDAL 3.0
    return 1.0 if crs.linear_units == "metre" else 2 * math.pi * 6378137 / 360.0
