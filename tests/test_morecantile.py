"""Tests for morecantile."""

import pytest

import mercantile
import morecantile


def test_default_grids():
    """Morecantile.default_grids should return the correct list of grids."""
    assert morecantile.default_grids == [
        "LINZAntarticaMapTilegrid",
        "EuropeanETRS89_LAEAQuad",
        "CanadianNAD83_LCC",
        "UPSArcticWGS84Quad",
        "NZTM2000",
        "UTM31WGS84Quad",
        "UPSAntarcticWGS84Quad",
        "WorldMercatorWGS84Quad",
        "WebMercatorQuad",
    ]


def test_tile_coordinates():
    """Test coordinates to tile index utils."""
    tms = morecantile.TileMatrixSet.load("WebMercatorQuad")
    assert tms.tile(-179, 85, 5) == (0, 0, 5)

    # Check equivalence between mercantile and morecantile
    # wlon, wlat = mercantile.xy(20.0, 15.0)
    assert tms.tile(20.0, 15.0, 5) == mercantile.tile(20.0, 15.0, 5)


@pytest.mark.parametrize(
    "args", [(486, 332, 10), [(486, 332, 10)], [morecantile.Tile(486, 332, 10)]]
)
def test_bounds(args):
    """
    TileMatrixSet.bounds should return the correct coordinates.

    test form https://github.com/mapbox/mercantile/blob/master/tests/test_funcs.py
    """
    expected = (-9.140625, 53.12040528310657, -8.7890625, 53.33087298301705)
    tms = morecantile.TileMatrixSet.load("WebMercatorQuad")
    bbox = tms.bounds(*args)
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
    TileMatrixSet.xy_bounds should return the correct coordinates.

    test form https://github.com/mapbox/mercantile/blob/master/tests/test_funcs.py
    """
    expected = (
        -1017529.7205322663,
        7005300.768279833,
        -978393.962050256,
        7044436.526761846,
    )
    tms = morecantile.TileMatrixSet.load("WebMercatorQuad")
    bounds = tms.xy_bounds(*args)
    for a, b in zip(expected, bounds):
        assert round(a - b, 7) == 0


def test_ul_tile():
    """
    TileMatrixSet.ul should return the correct coordinates.

    test form https://github.com/mapbox/mercantile/blob/master/tests/test_funcs.py
    """
    tms = morecantile.TileMatrixSet.load("WebMercatorQuad")
    xy = tms.ul(486, 332, 10)
    expected = (-9.140625, 53.33087298301705)
    for a, b in zip(expected, xy):
        assert round(a - b, 7) == 0


def test_projul_tile():
    """
    TileMatrixSet._ul should return the correct coordinates in input projection.

    test form https://github.com/mapbox/mercantile/blob/master/tests/test_funcs.py
    """
    tms = morecantile.TileMatrixSet.load("WebMercatorQuad")
    xy = tms._ul(486, 332, 10)
    expected = (-1017529.7205322663, 7044436.526761846)
    for a, b in zip(expected, xy):
        assert round(a - b, 7) == 0


def test_projtile():
    """TileSchema._tile should return the correct tile."""
    tms = morecantile.TileMatrixSet.load("WebMercatorQuad")
    assert tms._tile(1000, 1000, 1) == morecantile.Tile(1, 0, 1)


def test_feature():
    """TileSchema.feature should create proper geojson feature."""
    tms = morecantile.TileMatrixSet.load("WebMercatorQuad")
    feat = tms.feature(morecantile.Tile(1, 0, 1))
    assert feat["bbox"]
    assert feat["id"]
    assert feat["geometry"]
    assert len(feat["properties"].keys()) == 3

    feat = tms.feature(
        morecantile.Tile(1, 0, 1), precision=4, fid="1", props={"some": "thing"}
    )
    assert feat["bbox"]
    assert feat["id"] == "1"
    assert feat["geometry"]
    assert len(feat["properties"].keys()) == 4
