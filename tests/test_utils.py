"""test morecantile utils."""

import math

import pytest
from pyproj import CRS

from morecantile import utils


@pytest.mark.parametrize(
    "crs,unit",
    [
        (CRS.from_epsg(4326), 2 * math.pi * 6378137 / 360.0),
        (CRS.from_epsg(3857), 1.0),
        (CRS.from_epsg(2276), 0.30480060960121924),
        (CRS.from_epsg(2222), 0.3048),
        # Mars in Meter
        (
            CRS.from_proj4(
                "+proj=tmerc +lat_0=17 +lon_0=76.5 +k=0.9996 +x_0=0 +y_0=0 +a=3396190 +b=3376200 +units=m +no_defs"
            ),
            1.0,
        ),
        # Mars in Degrees
        # proj4 from https://github.com/AndrewAnnex/planetcantile/blob/5ea2577f5dc4a3bc91b0443ef0633a5f89b15e03/planetcantile/data/generate.py#L45-L47
        (
            CRS.from_proj4("+proj=longlat +R=3396190 +no_defs +type=crs"),
            2 * math.pi * 3396190 / 360.0,
        ),
    ],
)
def test_mpu(crs, unit):
    """test meters_per_unit."""
    assert utils.meters_per_unit(crs) == unit


@pytest.mark.parametrize(
    "lon1, lon2, contains", [(-180, 180, False), (179, -179, True)]
)
def test_lons_contain_antimeridian(lon1: float, lon2: float, contains: bool):
    assert utils.lons_contain_antimeridian(lon1, lon2) == contains
