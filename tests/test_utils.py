"""test morecantile utils."""

import math

import pytest
from pyproj import CRS

from morecantile import utils


@pytest.mark.parametrize(
    "epsg,unit",
    [
        (4326, 2 * math.pi * 6378137 / 360.0),
        (3857, 1.0),
        (2276, 0.30480060960121924),
        (2222, 0.3048),
    ],
)
def test_mpu(epsg, unit):
    """test meters_per_unit."""
    assert utils.meters_per_unit(CRS.from_epsg(epsg)) == unit
