"""Test TileMatrixSet model."""

import os
from collections.abc import Iterable

import pytest
from pydantic import ValidationError
from rasterio.crs import CRS

import morecantile
from morecantile.errors import DeprecationWarning, InvalidIdentifier
from morecantile.models import TileMatrix, TileMatrixSet

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


def test_tile_matrix_iter():
    """Test iterator"""
    tms = morecantile.tms.get("WebMercatorQuad")
    assert isinstance(tms, Iterable)
    for matrix in tms:
        assert isinstance(matrix, TileMatrix)


def test_tile_matrix():
    variable_matrix = {
        "type": "TileMatrixType",
        "identifier": "3",
        "scaleDenominator": 34942641.5017948,
        "topLeftCorner": [-180, 90],
        "tileWidth": 256,
        "tileHeight": 256,
        "matrixWidth": 16,
        "matrixHeight": 8,
        "variableMatrixWidth": [
            {
                "type": "VariableMatrixWidthType",
                "coalesce": 2,
                "minTileRow": 0,
                "maxTileRow": 0,
            },
            {
                "type": "VariableMatrixWidthType",
                "coalesce": 2,
                "minTileRow": 3,
                "maxTileRow": 3,
            },
        ],
    }
    with pytest.raises(ValidationError):
        TileMatrix(**variable_matrix)


def test_load():
    """Should raise an error when file not found."""
    with pytest.warns(DeprecationWarning):
        TileMatrixSet.load("WebMercatorQuad")

    with pytest.raises(InvalidIdentifier):
        TileMatrixSet.load("ANotValidName")


def test_findMatrix():
    """Should raise an error when TileMatrix is not found."""
    tms = morecantile.tms.get("WebMercatorQuad")
    m = tms.matrix(0)
    assert m.identifier == "0"

    with pytest.raises(Exception):
        tms.matrix(26)


def test_Custom():
    """Create custom TMS grid."""
    tms = morecantile.tms.get("WebMercatorQuad")

    # Web Mercator Extent
    extent = (-20037508.3427892, -20037508.3427892, 20037508.3427892, 20037508.3427892)
    custom_tms = TileMatrixSet.custom(extent, CRS.from_epsg(3857))

    assert tms.tile(20.0, 15.0, 5) == custom_tms.tile(20.0, 15.0, 5)

    wmMat = tms.matrix(5)
    cusMat = custom_tms.matrix(5)
    assert wmMat.matrixWidth == cusMat.matrixWidth
    assert wmMat.matrixHeight == cusMat.matrixHeight
    assert round(wmMat.scaleDenominator, 6) == round(cusMat.scaleDenominator, 6)
    assert round(wmMat.topLeftCorner[0], 6) == round(cusMat.topLeftCorner[0], 6)

    extent = (-180.0, -85.051128779806, 180.0, 85.051128779806)
    custom_tms = TileMatrixSet.custom(
        extent, CRS.from_epsg(3857), extent_crs=CRS.from_epsg(4326)
    )

    assert tms.tile(20.0, 15.0, 5) == custom_tms.tile(20.0, 15.0, 5)

    wmMat = tms.matrix(5)
    cusMat = custom_tms.matrix(5)
    assert wmMat.matrixWidth == cusMat.matrixWidth
    assert wmMat.matrixHeight == cusMat.matrixHeight
    assert round(wmMat.scaleDenominator, 6) == round(cusMat.scaleDenominator, 6)
    assert round(wmMat.topLeftCorner[0], 6) == round(cusMat.topLeftCorner[0], 6)
