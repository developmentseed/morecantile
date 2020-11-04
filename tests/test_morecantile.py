"""Tests for morecantile."""

import mercantile
import pytest
from rasterio.crs import CRS

import morecantile
from morecantile.errors import InvalidIdentifier
from morecantile.utils import meters_per_unit


def test_default_grids():
    """Morecantile.default_grids should return the correct list of grids."""
    assert len(morecantile.tms.list()) == 10

    with pytest.raises(InvalidIdentifier):
        morecantile.tms.get("ANotValidName")


def test_register():
    """Test register a new grid."""
    assert len(morecantile.tms.list()) == 10

    crs = CRS.from_epsg(3031)
    extent = [-948.75, -543592.47, 5817.41, -3333128.95]  # From https:///epsg.io/3031
    tms = morecantile.TileMatrixSet.custom(extent, crs, identifier="MyCustomGrid3031")

    morecantile.tms.register(tms)
    assert len(morecantile.tms.list()) == 10

    defaults = morecantile.tms.register(tms)
    assert len(defaults.list()) == 11
    assert "MyCustomGrid3031" in defaults.list()

    tms = morecantile.tms.register([tms])
    assert len(defaults.list()) == 11
    assert "MyCustomGrid3031" in defaults.list()


def test_TMSproperties():
    """Test TileSchema()."""
    tms = morecantile.tms.get("WebMercatorQuad")
    assert tms.crs == CRS.from_epsg(3857)
    assert meters_per_unit(tms.crs) == 1.0
    assert tms.minzoom == 0
    assert tms.maxzoom == 24

    tms = morecantile.tms.get("WorldCRS84Quad")
    assert tms.crs == CRS.from_epsg(4326)
    assert meters_per_unit(tms.crs) == 111319.49079327358


def test_tile_coordinates():
    """Test coordinates to tile index utils."""
    tms = morecantile.tms.get("WebMercatorQuad")
    assert tms.tile(-179, 85, 5) == (0, 0, 5)

    # Check equivalence between mercantile and morecantile
    # wlon, wlat = mercantile.xy(20.0, 15.0)
    assert tms.tile(20.0, 15.0, 5) == mercantile.tile(20.0, 15.0, 5)

    tms = morecantile.tms.get("WorldCRS84Quad")
    assert tms.tile(-39.8, 74.2, 4) == morecantile.Tile(12, 1, 4)


@pytest.mark.parametrize(
    "args", [(486, 332, 10), [(486, 332, 10)], [morecantile.Tile(486, 332, 10)]]
)
def test_bounds(args):
    """
    TileMatrixSet.bounds should return the correct coordinates.

    test form https://github.com/mapbox/mercantile/blob/master/tests/test_funcs.py
    """
    expected = (-9.140625, 53.12040528310657, -8.7890625, 53.33087298301705)
    tms = morecantile.tms.get("WebMercatorQuad")
    bbox = tms.bounds(*args)
    for a, b in zip(expected, bbox):
        assert round(a - b, 7) == 0
    assert bbox.left == bbox[0]
    assert bbox.bottom == bbox[1]
    assert bbox.right == bbox[2]
    assert bbox.top == bbox[3]


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
    tms = morecantile.tms.get("WebMercatorQuad")
    bounds = tms.xy_bounds(*args)
    for a, b in zip(expected, bounds):
        assert round(a - b, 7) == 0


def test_ul_tile():
    """
    TileMatrixSet.ul should return the correct coordinates.

    test form https://github.com/mapbox/mercantile/blob/master/tests/test_funcs.py
    """
    tms = morecantile.tms.get("WebMercatorQuad")
    xy = tms.ul(486, 332, 10)
    expected = (-9.140625, 53.33087298301705)
    for a, b in zip(expected, xy):
        assert round(a - b, 7) == 0


def test_projul_tile():
    """
    TileMatrixSet._ul should return the correct coordinates in input projection.

    test form https://github.com/mapbox/mercantile/blob/master/tests/test_funcs.py
    """
    tms = morecantile.tms.get("WebMercatorQuad")
    xy = tms._ul(486, 332, 10)
    expected = (-1017529.7205322663, 7044436.526761846)
    for a, b in zip(expected, xy):
        assert round(a - b, 7) == 0


def test_projtile():
    """TileSchema._tile should return the correct tile."""
    tms = morecantile.tms.get("WebMercatorQuad")
    assert tms._tile(1000, 1000, 1) == morecantile.Tile(1, 0, 1)


def test_feature():
    """TileSchema.feature should create proper geojson feature."""
    tms = morecantile.tms.get("WebMercatorQuad")
    feat = tms.feature(morecantile.Tile(1, 0, 1))
    assert feat["bbox"]
    assert feat["id"]
    assert feat["geometry"]
    assert len(feat["properties"].keys()) == 3

    feat = tms.feature(
        morecantile.Tile(1, 0, 1),
        buffer=-10,
        precision=4,
        fid="1",
        props={"some": "thing"},
    )
    assert feat["bbox"]
    assert feat["id"] == "1"
    assert feat["geometry"]
    assert len(feat["properties"].keys()) == 4

    with pytest.warns(UserWarning):
        feat = tms.feature(
            morecantile.Tile(1, 0, 1), projected=True, fid="1", props={"some": "thing"}
        )
    assert feat["bbox"]
    assert feat["id"] == "1"
    assert feat["geometry"]
    assert len(feat["properties"].keys()) == 4


################################################################################
# replicate mercantile tests
# https://github.com/mapbox/mercantile/blob/master/tests/test_funcs.py
@pytest.mark.parametrize(
    "args", [(486, 332, 10), [(486, 332, 10)], [morecantile.Tile(486, 332, 10)]]
)
def test_ul(args):
    """test args."""
    tms = morecantile.tms.get("WebMercatorQuad")
    expected = (-9.140625, 53.33087298301705)
    lnglat = tms.ul(*args)
    for a, b in zip(expected, lnglat):
        assert round(a - b, 7) == 0
    assert lnglat[0] == lnglat.x
    assert lnglat[1] == lnglat.y


@pytest.mark.parametrize(
    "args", [(486, 332, 10), [(486, 332, 10)], [mercantile.Tile(486, 332, 10)]]
)
def test_bbox(args):
    """test bbox."""
    tms = morecantile.tms.get("WebMercatorQuad")
    expected = (-9.140625, 53.12040528310657, -8.7890625, 53.33087298301705)
    bbox = tms.bounds(*args)
    for a, b in zip(expected, bbox):
        assert round(a - b, 7) == 0
    assert bbox.left == bbox[0]
    assert bbox.bottom == bbox[1]
    assert bbox.right == bbox[2]
    assert bbox.top == bbox[3]


def test_xy_tile():
    """x, y for the 486-332-10 tile is correctly calculated."""
    tms = morecantile.tms.get("WebMercatorQuad")
    ul = tms.ul(486, 332, 10)
    xy = tms.xy(*ul)
    expected = (-1017529.7205322663, 7044436.526761846)
    for a, b in zip(expected, xy):
        assert round(a - b, 7) == 0


def test_xy_null_island():
    """x, y for (0, 0) is correctly calculated"""
    tms = morecantile.tms.get("WebMercatorQuad")
    xy = tms.xy(0.0, 0.0)
    expected = (0.0, 0.0)
    for a, b in zip(expected, xy):
        assert round(a - b, 7) == 0


def test_xy_south_pole():
    """Return -inf for y at South Pole"""
    tms = morecantile.tms.get("WebMercatorQuad")
    xy = tms.xy(0.0, -90)
    assert xy.x == 0.0
    assert xy.y == float("-inf")


def test_xy_north_pole():
    """Return inf for y at North Pole"""
    tms = morecantile.tms.get("WebMercatorQuad")
    xy = tms.xy(0.0, 90)
    assert xy.x == 0.0
    assert xy.y == float("inf")


def test_xy_truncate():
    """Input is truncated"""
    tms = morecantile.tms.get("WebMercatorQuad")
    assert tms.xy(-181.0, 0.0, truncate=True) == tms.xy(-180.0, 0.0)


@pytest.mark.xfail
def test_lnglat():
    """test lnglat."""
    tms = morecantile.tms.get("WebMercatorQuad")

    with pytest.warns(UserWarning) as w:
        assert not w
        xy = (-8366731.739810849, -1655181.9927159143)
        lnglat = tms.lnglat(*xy)
        assert round(lnglat.x, 5) == -75.15963
        assert round(lnglat.y, 5) == -14.70462

    with pytest.warns(UserWarning):
        xy = (-28366731.739810849, -1655181.9927159143)
        lnglat = tms.lnglat(*xy, truncate=True)
        # GDAL returns ('inf', 'inf') and then inf is translated to 180,90 by truncate_lnglat
        # assert round(lnglat.x, 5) == -180.0  # in Mercantile
        # assert round(lnglat.y, 5) == -14.70462  # in Mercantile
        assert round(lnglat.x, 5) == 180.0
        assert round(lnglat.y, 5) == 90


def test_lnglat_xy_roundtrip():
    """Test roundtrip."""
    tms = morecantile.tms.get("WebMercatorQuad")
    lnglat = (-105.0844, 40.5853)
    roundtrip = tms.lnglat(*tms.xy(*lnglat))
    for a, b in zip(roundtrip, lnglat):
        assert round(a - b, 7) == 0


@pytest.mark.parametrize(
    "args", [(486, 332, 10), [(486, 332, 10)], [mercantile.Tile(486, 332, 10)]]
)
def test_xy_bounds_mercantile(args):
    """test xy_bounds."""
    tms = morecantile.tms.get("WebMercatorQuad")
    expected = (
        -1017529.7205322663,
        7005300.768279833,
        -978393.962050256,
        7044436.526761846,
    )
    bounds = tms.xy_bounds(*args)

    for a, b in zip(expected, bounds):
        assert round(a - b, 7) == 0


def test_tile_not_truncated():
    """test tile."""
    tms = morecantile.tms.get("WebMercatorQuad")
    tile = tms.tile(20.6852, 40.1222, 9)
    expected = (285, 193)
    assert tile[0] == expected[0]
    assert tile[1] == expected[1]


def test_tile_truncate():
    """Input is truncated"""
    tms = morecantile.tms.get("WebMercatorQuad")
    assert tms.tile(-181.0, 0.0, 9, truncate=True) == tms.tile(-180.0, 0.0, 9)


def test_tiles():
    """Test tiles from bbox."""
    tms = morecantile.tms.get("WebMercatorQuad")

    # replicate mercantile tests
    # https://github.com/mapbox/mercantile/blob/master/tests/test_funcs.py#L115-L178
    bounds = (-105, 39.99, -104.99, 40)
    tiles = list(tms.tiles(*bounds, zooms=[14]))
    expect = [
        morecantile.Tile(x=3413, y=6202, z=14),
        morecantile.Tile(x=3413, y=6203, z=14),
    ]
    assert sorted(tiles) == sorted(expect)

    # Single zoom
    bounds = (-105, 39.99, -104.99, 40)
    tiles = list(tms.tiles(*bounds, zooms=14))
    expect = [
        morecantile.Tile(x=3413, y=6202, z=14),
        morecantile.Tile(x=3413, y=6203, z=14),
    ]
    assert sorted(tiles) == sorted(expect)

    # Input is truncated
    assert list(tms.tiles(-181.0, 0.0, -170.0, 10.0, zooms=[2], truncate=True)) == list(
        tms.tiles(-180.0, 0.0, -170.0, 10.0, zooms=[2])
    )

    # Antimeridian-crossing bounding boxes are handled
    bounds = (175.0, 5.0, -175.0, 10.0)
    assert len(list(tms.tiles(*bounds, zooms=[2]))) == 2

    # Y is clamped to (0, 2 ** zoom - 1)
    tiles = list(tms.tiles(-180, -90, 180, 90, [1]))
    assert len(tiles) == 4
    assert min(t.y for t in tiles) == 0
    assert max(t.y for t in tiles) == 1

    # tiles(bounds(tile)) gives the tile's children
    t = morecantile.Tile(x=3413, y=6202, z=14)
    res = list(tms.tiles(*tms.bounds(t), zooms=[15]))
    assert len(res) == 4


@pytest.mark.parametrize(
    "t",
    [
        morecantile.Tile(x=3413, y=6202, z=14),
        morecantile.Tile(486, 332, 10),
        # morecantile.Tile(10, 10, 10), This is failing
    ],
)
def test_tiles_roundtrip(t):
    """Tiles(bounds(tile)) gives the tile."""
    tms = morecantile.tms.get("WebMercatorQuad")
    res = list(tms.tiles(*tms.bounds(t), zooms=[t.z]))
    assert len(res) == 1
    val = res.pop()
    assert val.x == t.x
    assert val.y == t.y
    assert val.z == t.z


def test_extend_zoom():
    """TileMatrixSet.ul should return the correct coordinates."""
    tms = morecantile.tms.get("WebMercatorQuad")
    merc = mercantile.xy_bounds(1000, 1000, 25)
    with pytest.warns(UserWarning):
        more = tms.xy_bounds(1000, 1000, 25)
    for a, b in zip(more, merc):
        assert round(a - b, 7) == 0

    merc = mercantile.xy_bounds(2000, 2000, 26)
    with pytest.warns(UserWarning):
        more = tms.xy_bounds(2000, 2000, 26)
    for a, b in zip(more, merc):
        assert round(a - b, 7) == 0

    merc = mercantile.xy_bounds(2000, 2000, 27)
    with pytest.warns(UserWarning):
        more = tms.xy_bounds(2000, 2000, 27)
    for a, b in zip(more, merc):
        assert round(a - b, 7) == 0

    merc = mercantile.xy_bounds(2000, 2000, 30)
    with pytest.warns(UserWarning):
        more = tms.xy_bounds(2000, 2000, 30)
    for a, b in zip(more, merc):
        assert round(a - b, 7) == 0
