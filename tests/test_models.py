"""Test TileMatrixSet model."""

import os
import pytest

from morecantile.models import TileMatrixSet, NotAValidName
from rasterio.crs import CRS

data_dir = os.path.join(os.path.dirname(__file__), "../morecantile/data")
tilesets = [
    os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith(".json")
]


@pytest.mark.parametrize("tileset", tilesets)
def test_tile_matrix_set(tileset):
    """Load TileMatrixSet in models."""
    # Confirm model validation is working
    ts = TileMatrixSet.parse_file(tileset)
    # This would fail if `supportedCRS` isn't supported by GDAL/Rasterio
    epsg = ts.crs
    isinstance(epsg, CRS)


def test_load():
    """Should raise an error when file not found."""
    TileMatrixSet.load("WebMercatorQuad")
    with pytest.raises(NotAValidName):
        TileMatrixSet.load("ANotValidName")


def test_findMatrix():
    """Should raise an error when TileMatrix is not found."""
    tms = TileMatrixSet.load("WebMercatorQuad")
    m = tms.matrix(0)
    assert m.identifier == "0"

    with pytest.raises(Exception):
        tms.matrix(26)
