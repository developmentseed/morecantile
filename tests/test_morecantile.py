"""Tests for morecantile."""

import pytest

import mercantile
import morecantile
from rasterio.crs import CRS


def test_default_grids():
    """Morecantile.default_grids should return the correct crs and metadata."""
    grid_info = morecantile.default_grids.get("WorldCRS84Quad")
    assert grid_info["crs"] == CRS.from_epsg(4326)
    with pytest.raises(Exception):
        morecantile.default_grids.get("WorldCRS84")


def test_tileschema():
    """Test TileSchema()."""
    ts = morecantile.TileSchema()
    assert ts.crs == CRS.from_epsg(3857)
    assert ts.meters_per_unit == 1.0

    args = morecantile.default_grids.get("WorldCRS84Quad")
    ts = morecantile.TileSchema(**args)
    assert ts.crs == CRS.from_epsg(4326)
    assert ts.matrix_scale == [2, 1]
    assert ts.meters_per_unit == 111319.49079327358

    # Define WebMercator Grid using WGS84 extent
    ts = morecantile.TileSchema(
        CRS.from_epsg(3857),
        extent=[-180.0, -85.051128779806, 180.0, 85.051128779806],
        extent_crs=CRS.from_epsg(4326),
    )
    for a, b in zip(mercantile.xy_bounds(0, 0, 0), ts.extent):
        assert round(a - b, 5) == 0


def test_tilematrix():
    """Test OGC TileMatric meta."""
    ts = morecantile.TileSchema()
    matrix = ts.get_ogc_tilematrix(0)
    assert matrix == {
        "type": "TileMatrixType",
        "identifier": "0",
        "scaleDenominator": 559082264.0287178,
        "topLeftCorner": [-20037508.342789244, 20037508.342789244],
        "tileWidth": 256,
        "tileHeight": 256,
        "matrixWidth": 1,
        "matrixHeight": 1,
    }

    args = morecantile.default_grids.get("WorldCRS84Quad")
    ts = morecantile.TileSchema(**args)
    matrix = ts.get_ogc_tilematrix(0)
    assert matrix == {
        "type": "TileMatrixType",
        "identifier": "0",
        "scaleDenominator": 279541132.0143589,
        "topLeftCorner": [-180.0, 90.0],
        "tileWidth": 256,
        "tileHeight": 256,
        "matrixWidth": 2,
        "matrixHeight": 1,
    }


def test_tile_coordinates():
    """Test coordinates to tile index utils."""
    ts = morecantile.TileSchema()
    assert ts.tile(-179, 85, 5) == (0, 0, 5)

    # Check equivalence between mercantile and morecantile
    # wlon, wlat = mercantile.xy(20.0, 15.0)
    assert ts.tile(20.0, 15.0, 5) == mercantile.tile(20.0, 15.0, 5)

    args = morecantile.default_grids.get("WorldCRS84Quad")
    ts = morecantile.TileSchema(**args)
    assert ts.tile(10.0, 10.0, 5) == morecantile.Tile(16, 14, 5)


@pytest.mark.parametrize(
    "args", [(486, 332, 10), [(486, 332, 10)], [morecantile.Tile(486, 332, 10)]]
)
def test_bounds(args):
    """
    TileSchema.bounds should return the correct coordinates.

    test form https://github.com/mapbox/mercantile/blob/master/tests/test_funcs.py
    """
    expected = (-9.140625, 53.12040528310657, -8.7890625, 53.33087298301705)
    ts = morecantile.TileSchema()
    bbox = ts.bounds(*args)
    for a, b in zip(expected, bbox):
        assert round(a - b, 7) == 0
    assert bbox.xmin == bbox[0]
    assert bbox.ymin == bbox[1]
    assert bbox.xmax == bbox[2]
    assert bbox.ymax == bbox[3]


@pytest.mark.parametrize(
    "args", [(486, 332, 10), [(486, 332, 10)], [morecantile.Tile(486, 332, 10)]]
)
def test_xy_bounds(args):
    """
    TileSchema.xy_bounds should return the correct coordinates.

    test form https://github.com/mapbox/mercantile/blob/master/tests/test_funcs.py
    """
    expected = (
        -1017529.7205322663,
        7005300.768279833,
        -978393.962050256,
        7044436.526761846,
    )
    ts = morecantile.TileSchema()
    bounds = ts.xy_bounds(*args)
    for a, b in zip(expected, bounds):
        assert round(a - b, 7) == 0


def test_ul_tile():
    """
    TileSchema.ul should return the correct coordinates.

    test form https://github.com/mapbox/mercantile/blob/master/tests/test_funcs.py
    """
    ts = morecantile.TileSchema()
    xy = ts.ul(486, 332, 10)
    expected = (-9.140625, 53.33087298301705)
    for a, b in zip(expected, xy):
        assert round(a - b, 7) == 0


def test_projul_tile():
    """
    TileSchema._ul should return the correct coordinates in input projection.

    test form https://github.com/mapbox/mercantile/blob/master/tests/test_funcs.py
    """
    ts = morecantile.TileSchema()
    xy = ts._ul(486, 332, 10)
    expected = (-1017529.7205322663, 7044436.526761846)
    for a, b in zip(expected, xy):
        assert round(a - b, 7) == 0


def test_projtile():
    """TileSchema._tile should return the correct tile."""
    ts = morecantile.TileSchema()
    assert ts._tile(1000, 1000, 1) == morecantile.Tile(1, 0, 1)


def test_feature():
    """TileSchema.feature should create proper geojson feature."""
    ts = morecantile.TileSchema()
    feat = ts.feature(morecantile.Tile(1, 0, 1))
    assert feat["bbox"]
    assert feat["id"]
    assert feat["geometry"]
    assert len(feat["properties"].keys()) == 2

    feat = ts.feature(
        morecantile.Tile(1, 0, 1), precision=4, fid="1", props={"some": "thing"}
    )
    assert feat["bbox"]
    assert feat["id"] == "1"
    assert feat["geometry"]
    assert len(feat["properties"].keys()) == 3
