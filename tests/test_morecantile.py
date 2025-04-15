"""Tests for morecantile."""

import math
import warnings

import mercantile
import pytest
from pyproj import CRS

import morecantile
from morecantile.errors import (
    InvalidIdentifier,
    InvalidZoomError,
    PointOutsideTMSBounds,
)
from morecantile.utils import is_power_of_two, meters_per_unit

DEFAULT_GRID_COUNT = 13
TESTING_GRID_COUNT = 1


def test_default_grids():
    """Morecantile.default_grids should return the correct list of grids."""
    assert len(morecantile.tms.list()) == DEFAULT_GRID_COUNT + TESTING_GRID_COUNT

    with pytest.raises(InvalidIdentifier):
        morecantile.tms.get("ANotValidName")


def test_register():
    """Test register a new grid."""
    assert len(morecantile.tms.list()) == DEFAULT_GRID_COUNT + TESTING_GRID_COUNT

    crs = CRS.from_epsg(3031)
    extent = [-948.75, -543592.47, 5817.41, -3333128.95]  # From https:///epsg.io/3031
    tms = morecantile.TileMatrixSet.custom(extent, crs, id="MyCustomGrid3031")

    # Make sure we don't update the default tms (frozen set)
    _ = morecantile.tms.register({"MyCustomGrid3031": tms})
    assert len(morecantile.tms.list()) == DEFAULT_GRID_COUNT + TESTING_GRID_COUNT

    defaults = morecantile.tms.register({"MyCustomGrid3031": tms})
    assert len(defaults.list()) == DEFAULT_GRID_COUNT + TESTING_GRID_COUNT + 1
    assert "MyCustomGrid3031" in defaults.list()

    # Check it will raise an exception if TMS is already registered
    with pytest.raises(InvalidIdentifier):
        defaults = defaults.register({"MyCustomGrid3031": tms})

    # Do not raise is overwrite=True
    defaults = defaults.register({"MyCustomGrid3031": tms}, overwrite=True)
    assert len(defaults.list()) == DEFAULT_GRID_COUNT + TESTING_GRID_COUNT + 1

    # add tms in morecantile defaults (not something to do anyway)
    epsg3031 = morecantile.TileMatrixSet.custom(extent, crs, id="epsg3031")
    morecantile.defaults.default_tms["epsg3031"] = epsg3031
    assert len(morecantile.defaults.default_tms.keys()) == DEFAULT_GRID_COUNT + 1

    # make sure updating the default_tms dict has no effect on the default TileMatrixSets
    assert len(morecantile.tms.list()) == DEFAULT_GRID_COUNT + TESTING_GRID_COUNT

    # Update internal TMS dict
    morecantile.tms.tms["MyCustomGrid3031"] = tms
    assert len(morecantile.tms.list()) == DEFAULT_GRID_COUNT + TESTING_GRID_COUNT + 1

    # make sure it doesn't propagate to the default dict
    assert "MyCustomGrid3031" not in morecantile.defaults.default_tms


def test_TMSproperties():
    """Test TileSchema()."""
    tms = morecantile.tms.get("WebMercatorQuad")
    assert tms.crs._pyproj_crs == CRS.from_epsg(3857)
    assert meters_per_unit(tms.crs._pyproj_crs) == 1.0
    assert tms.minzoom == 0
    assert tms.maxzoom == 24


def test_tile_coordinates():
    """Test coordinates to tile index utils."""
    tms = morecantile.tms.get("WebMercatorQuad")
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
    tms = morecantile.tms.get("WebMercatorQuad")
    bbox = tms.bounds(*args)
    for a, b in zip(expected, bbox):
        assert round(a - b, 6) == 0
    assert bbox.left == bbox[0]
    assert bbox.bottom == bbox[1]
    assert bbox.right == bbox[2]
    assert bbox.top == bbox[3]


@pytest.mark.parametrize(
    ("tile_args", "identifier"),
    [
        ((486, 332, 10), "WebMercatorQuad"),
        (morecantile.Tile(486, 332, 10), "WebMercatorQuad"),

        # bottomLeft tests. y should be matrixWidth-topLeft-1 to produce the same value as topLeft
        ((486, 1023 - 332, 10), "WebMercatorQuadBottomLeft"),
        (morecantile.Tile(486, 1023 - 332, 10), "WebMercatorQuadBottomLeft"),

    ],
)
def test_xy_bounds(tile_args, identifier):
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
    tms = morecantile.tms.get(identifier)
    bounds = tms.xy_bounds(*tile_args)
    for a, b in zip(expected, bounds):
        assert round(a - b, 6) == 0


@pytest.mark.parametrize(
    ("tile_args", "identifier", "expected"),
    [
        ((486, 332, 10), "WebMercatorQuad", (-9.140625, 53.33087298301705)),
        (morecantile.Tile(486, 332, 10), "WebMercatorQuad", (-9.140625, 53.33087298301705)),

        ((486, 691, 10), "WebMercatorQuadBottomLeft", (-9.140625, 53.33087298301705)),
        (morecantile.Tile(486, 691, 10), "WebMercatorQuadBottomLeft", (-9.140625, 53.33087298301705)),
    ],
)
def test_ul_tile(tile_args, identifier, expected):
    """
    TileMatrixSet.ul should return the correct coordinates.

    test form https://github.com/mapbox/mercantile/blob/master/tests/test_funcs.py
    """
    tms = morecantile.tms.get(identifier)
    xy = tms.ul(*tile_args)
    print(xy)
    for a, b in zip(expected, xy):
        assert round(a - b, 6) == pytest.approx(0)


def test_projul_tile():
    """
    TileMatrixSet._ul should return the correct coordinates in input projection.

    test form https://github.com/mapbox/mercantile/blob/master/tests/test_funcs.py
    """
    tms = morecantile.tms.get("WebMercatorQuad")
    xy = tms._ul(486, 332, 10)
    expected = (-1017529.7205322663, 7044436.526761846)
    for a, b in zip(expected, xy):
        assert round(a - b, 6) == 0


@pytest.mark.parametrize(
    ("x", "y", "zoom", "identifier", "expected_tile"),
    [
        (1000, 1000, 1, 'WebMercatorQuad', morecantile.Tile(1, 0, 1)),
        (1000, 1000, 1, 'WebMercatorQuadBottomLeft', morecantile.Tile(1, 1, 1))

    ])
def test_projtile(x, y, zoom, identifier, expected_tile):
    """TileSchema._tile should return the correct tile."""
    tms = morecantile.tms.get(identifier)
    assert tms._tile(x, y, zoom) == expected_tile


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
    ("tile_args", "identifier", "expected"),
    [

        ((486, 332, 10), "WebMercatorQuad", (-9.140625, 53.33087298301705)),
        (morecantile.Tile(486, 332, 10), "WebMercatorQuad", (-9.140625, 53.33087298301705)),

        ((486, 691, 10), "WebMercatorQuadBottomLeft", (-9.140625, 53.33087298301705)),
        (morecantile.Tile(486, 691, 10), "WebMercatorQuadBottomLeft", (-9.140625, 53.33087298301705)),

        (morecantile.Tile(0, 0, 0), "WebMercatorQuad", (-180, 85.0511287798066)),
        (morecantile.Tile(0, 0, 0), "WebMercatorQuadBottomLeft", (-180, 85.0511287798066)),

    ],
)
def test_ul(tile_args, identifier, expected):
    """test args."""
    tms = morecantile.tms.get(identifier)
    lnglat = tms.ul(*tile_args)
    for a, b in zip(expected, lnglat):
        assert round(a - b, 6) == 0
    assert lnglat[0] == lnglat.x
    assert lnglat[1] == lnglat.y


@pytest.mark.parametrize(
    ("topLeft_Tile", "bottomLeft_Tile"),
    [
        (morecantile.Tile(10, 10, 10), morecantile.Tile(10, 1013, 10)),
        (morecantile.Tile(10, 1013, 10), morecantile.Tile(10, 10, 10)),

        # Check the Origin points
        (morecantile.Tile(0, 0, 10), morecantile.Tile(0, 1023, 10)),
        (morecantile.Tile(0, 1023, 10), morecantile.Tile(0, 0, 10)),

        # Check the end points
        (morecantile.Tile(1023, 0, 10), morecantile.Tile(1023, 1023, 10)),
        (morecantile.Tile(1023, 1023, 10), morecantile.Tile(1023, 0, 10)),

        # Zoom=0
        (morecantile.Tile(0, 0, 0), morecantile.Tile(0, 0, 0)),

        # zoom=1 on both edges of the zoom level
        (morecantile.Tile(0, 0, 1), morecantile.Tile(0, 1, 1)),
        (morecantile.Tile(0, 1, 1), morecantile.Tile(0, 0, 1)),

        # zoom=14 near the middle
        (morecantile.Tile(x=3413, y=6202, z=14), morecantile.Tile(x=3413, y=10181, z=14))
    ]
)
def test_topLeft_BottomLeft_bounds_equal_bounds(topLeft_Tile, bottomLeft_Tile):
    tmsTop = morecantile.tms.get("WebMercatorQuad")
    tmsBottom = morecantile.tms.get("WebMercatorQuadBottomLeft")

    bounds = tmsTop.xy_bounds(topLeft_Tile)
    bounds2 = tmsBottom.xy_bounds(bottomLeft_Tile)
    for a, b in zip(bounds, bounds2):
        assert round(a - b, 6) == 0


@pytest.mark.parametrize(
    ("topLeft_Tile", "bottomLeft_Tile"),
    [
        (morecantile.Tile(10, 10, 10), morecantile.Tile(10, 1013, 10)),
        (morecantile.Tile(0, 0, 10), morecantile.Tile(0, 1023, 10)),

        # Check the oring tile with zoom=0
        (morecantile.Tile(0, 0, 0), morecantile.Tile(0, 0, 0)),

        # Origin tile of zoom=1
        (morecantile.Tile(0, 0, 1), morecantile.Tile(0, 1, 1)),
        # last tile of zoom=1
        (morecantile.Tile(1, 1, 1), morecantile.Tile(1, 0, 1)),
        (morecantile.Tile(1, 1, 1), morecantile.Tile(1, 0, 1)),

        # zoom=14 near the middle
        (morecantile.Tile(x=3413, y=6202, z=14), morecantile.Tile(x=3413, y=10181, z=14))

    ]
)
@pytest.mark.parametrize("identifier", ["WebMercatorQuad", "WebMercatorQuadBottomLeft"])
def test_translate_cornerOfOrigin_Tile(topLeft_Tile, bottomLeft_Tile, identifier):
    tmsTop = morecantile.tms.get(identifier)
    matrix = tmsTop.matrix(topLeft_Tile.z)

    translated_tile = matrix.translate_cornerOfOrigin_Tile(topLeft_Tile)
    assert translated_tile == bottomLeft_Tile

    untranslated_tile = matrix.translate_cornerOfOrigin_Tile(translated_tile)
    assert untranslated_tile == topLeft_Tile


@pytest.mark.parametrize(
    ("tile_args", "identifier", "expected"),
    [
        ((486, 332, 10), "WebMercatorQuad", (-9.140625, 53.12040528310657, -8.7890625, 53.33087298301705)),
        (morecantile.Tile(486, 332, 10), "WebMercatorQuad",
         (-9.140625, 53.12040528310657, -8.7890625, 53.33087298301705)),

        ((486, 691, 10), "WebMercatorQuadBottomLeft", (-9.140625, 53.12040528310657, -8.7890625, 53.33087298301705)),
        (morecantile.Tile(486, 691, 10), "WebMercatorQuadBottomLeft",
         (-9.140625, 53.12040528310657, -8.7890625, 53.33087298301705)),
    ],
)
def test_bbox(tile_args, identifier, expected):
    """test bbox."""
    tms = morecantile.tms.get(identifier)
    bbox = tms.bounds(*tile_args)
    for a, b in zip(expected, bbox):
        assert round(a - b, 6) == 0
    assert bbox.left == bbox[0]
    assert bbox.bottom == bbox[1]
    assert bbox.right == bbox[2]
    assert bbox.top == bbox[3]


@pytest.mark.parametrize(
    ("tile", "identifier"),
    [
        (morecantile.Tile(486, 332, 10), "WebMercatorQuad"),
        (morecantile.Tile(486, 332, 10), "WebMercatorQuadBottomLeft"),
        # check origin
        (morecantile.Tile(0, 0, 0), "WebMercatorQuad"),
        (morecantile.Tile(0, 0, 0), "WebMercatorQuadBottomLeft"),
        # Check final tiles
        (morecantile.Tile(1, 1, 1), "WebMercatorQuad"),
        (morecantile.Tile(1, 1, 1), "WebMercatorQuadBottomLeft"),
    ])
def test_bounding_box_ulurlllr(tile, identifier):
    """Test that bounds and georeference functions return the same values"""
    tms = morecantile.tms.get(identifier)
    bbox = tms.bounds(*tile)
    ul = tms.ul(*tile)
    ll = tms.ll(*tile)
    ur = tms.ur(*tile)
    lr = tms.lr(*tile)

    assert (ul.x, ul.y) == (bbox.left, bbox.top)
    assert (ll.x, ll.y) == (bbox.left, bbox.bottom)
    assert (ur.x, ur.y) == (bbox.right, bbox.top)
    assert (lr.x, lr.y) == (bbox.right, bbox.bottom)


@pytest.mark.parametrize(
    ("tile", "identifier"),
    [
        (morecantile.Tile(486, 332, 10), "WebMercatorQuad"),
        (morecantile.Tile(486, 332, 10), "WebMercatorQuadBottomLeft"),
        # check origin
        (morecantile.Tile(0, 0, 0), "WebMercatorQuad"),
        (morecantile.Tile(0, 0, 0), "WebMercatorQuadBottomLeft"),
        # Check final tiles
        (morecantile.Tile(1, 1, 1), "WebMercatorQuad"),
        (morecantile.Tile(1, 1, 1), "WebMercatorQuadBottomLeft"),
    ])
def test_tms_bounding_box_ulurlllr(tile, identifier):
    """Test that xy_bounds and tms functions return the same values"""
    tms = morecantile.tms.get(identifier)
    bbox = tms.xy_bounds(*tile)
    ul = tms._ul(*tile)
    ll = tms._ll(*tile)
    ur = tms._ur(*tile)
    lr = tms._lr(*tile)

    assert (ul.x, ul.y) == (bbox.left, bbox.top)
    assert (ll.x, ll.y) == (bbox.left, bbox.bottom)
    assert (ur.x, ur.y) == (bbox.right, bbox.top)
    assert (lr.x, lr.y) == (bbox.right, bbox.bottom)


@pytest.mark.parametrize(
    ("tile", "identifier"),
    [
        (morecantile.Tile(486, 332, 10), "WebMercatorQuad"),
        (morecantile.Tile(486, 332, 10), "WebMercatorQuadBottomLeft"),
        # check origin
        (morecantile.Tile(0, 0, 0), "WebMercatorQuad"),
        (morecantile.Tile(0, 0, 0), "WebMercatorQuadBottomLeft"),
        # Check final tiles
        (morecantile.Tile(1, 1, 1), "WebMercatorQuad"),
        (morecantile.Tile(1, 1, 1), "WebMercatorQuadBottomLeft"),
    ])
def test_origin_coords(tile, identifier):
    tms = morecantile.tms.get(identifier)
    matrix = tms.matrix(tile.z)
    origin = tms.origin_coords(*tile)
    across = tms.origin_coords_across(*tile)

    if matrix.cornerOfOrigin == 'topLeft':
        assert origin == tms.ul(*tile)
        assert across == tms.lr(*tile)
    elif matrix.cornerOfOrigin == 'bottomLeft':
        assert origin == tms.ll(*tile)
        assert across == tms.ur(*tile)
    else:
        raise NotImplementedError()


@pytest.mark.parametrize(
    ("tile_args", "identifier", "expected"),
    [
        (morecantile.Tile(486, 332, 10), "WebMercatorQuad", (-1017529.7205322663, 7044436.526761846)),
        (morecantile.Tile(10, 10, 10), "WebMercatorQuad", (-19646150.757969137, 19646150.757969007)),
        (morecantile.Tile(10, 1013, 10), "WebMercatorQuadBottomLeft", (-19646150.757969137, 19646150.757969007)),

    ]
)
def test_xy_tile(tile_args, identifier, expected):
    """x, y for the 486-332-10 tile is correctly calculated."""
    tms = morecantile.tms.get(identifier)
    ul = tms.ul(*tile_args)
    xy = tms.xy(*ul)
    for a, b in zip(expected, xy):
        assert round(a - b, 6) == 0


@pytest.mark.parametrize("identifier", ["WebMercatorQuad", "WebMercatorQuadBottomLeft"])
def test_xy_null_island(identifier):
    """x, y for (0, 0) is correctly calculated"""
    tms = morecantile.tms.get(identifier)
    xy = tms.xy(0.0, 0.0)
    expected = (0.0, 0.0)
    for a, b in zip(expected, xy):
        assert round(a - b, 6) == 0


@pytest.mark.xfail
def test_xy_south_pole():
    """Return -inf for y at South Pole

    Note: mercantile returns (0.0, inf)
    """
    tms = morecantile.tms.get("WebMercatorQuad")
    with pytest.warns(PointOutsideTMSBounds):
        xy = tms.xy(0.0, -90)
        assert xy.x == 0.0
        assert xy.y == float("inf")


@pytest.mark.xfail
def test_xy_north_pole():
    """Return inf for y at North Pole.

    Note: mercantile returns (0.0, -inf)
    """
    tms = morecantile.tms.get("WebMercatorQuad")
    with pytest.warns(PointOutsideTMSBounds):
        xy = tms.xy(0.0, 90)
        assert xy.x == 0.0
        assert xy.y == float("inf")


@pytest.mark.parametrize("identifier", ["WebMercatorQuad", "WebMercatorQuadBottomLeft"])
def test_xy_truncate(identifier):
    """Input is truncated"""
    tms = morecantile.tms.get(identifier)
    assert tms.xy(-181.0, 0.0, truncate=True) == tms.xy(tms.bbox.left, 0.0)


@pytest.mark.xfail
def test_lnglat():
    """test lnglat."""
    tms = morecantile.tms.get("WebMercatorQuad")

    # Make sure not warning is raised
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        xy = (-8366731.739810849, -1655181.9927159143)
        lnglat = tms.lnglat(*xy)
        assert round(lnglat.x, 5) == -75.15963
        assert round(lnglat.y, 5) == -14.70462

    with pytest.warns(PointOutsideTMSBounds):
        xy = (-28366731.739810849, -1655181.9927159143)
        lnglat = tms.lnglat(*xy, truncate=True)
        assert round(lnglat.x, 5) == -180.0  # in Mercantile (105.17731 in Morecantile)
        assert round(lnglat.y, 5) == -14.70462  # in Mercantile


@pytest.mark.parametrize("tms_name", morecantile.tms.list())
def test_axis_inverted(tms_name):
    """Test axis inversion check"""
    tms = morecantile.tms.get(tms_name)
    if tms.orderedAxes:
        assert morecantile.models.crs_axis_inverted(
            tms.crs._pyproj_crs
        ) == morecantile.models.ordered_axis_inverted(tms.orderedAxes)


def test_lnglat_gdal3():
    """test lnglat."""
    # PROJ>=7 returns (105.17731317609572, -14.704620000000013)
    tms = morecantile.tms.get("WebMercatorQuad")
    with pytest.warns(PointOutsideTMSBounds):
        xy = (-28366731.739810849, -1655181.9927159143)
        lnglat = tms.lnglat(*xy, truncate=True)
        assert round(lnglat.x, 5) == 105.17731
        assert round(lnglat.y, 5) == -14.70462


@pytest.mark.parametrize("identifier", ["WebMercatorQuad", "WebMercatorQuadBottomLeft"])
def test_lnglat_xy_roundtrip(identifier):
    """Test roundtrip."""
    tms = morecantile.tms.get(identifier)
    lnglat = (-105.0844, 40.5853)
    roundtrip = tms.lnglat(*tms.xy(*lnglat))
    for a, b in zip(roundtrip, lnglat):
        assert round(a - b, 6) == 0


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
        assert round(a - b, 6) == 0


@pytest.mark.parametrize(
    ("identifier", "expected_tile"),
    (

            (["WebMercatorQuad", morecantile.Tile(285, 193, 9)]),
            (["WebMercatorQuadBottomLeft", morecantile.Tile(285, 318, 9)])

    )
)
def test_tile_not_truncated(identifier, expected_tile):
    """test tile."""
    tms = morecantile.tms.get(identifier)
    tile = tms.tile(20.6852, 40.1222, 9)
    assert tile == expected_tile


@pytest.mark.parametrize("identifier", ["WebMercatorQuad", "WebMercatorQuadBottomLeft"])
def test_tile_truncate(identifier):
    """Input is truncated"""
    tms = morecantile.tms.get(identifier)
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

    assert list(tms.tiles(-180.0, -90.0, 180.0, 90.0, zooms=[0])) == [
        morecantile.Tile(x=0, y=0, z=0)
    ]
    assert list(tms.tiles(-180.0, -90.0, 180.0, 90.0, zooms=[0], truncate=True)) == [
        morecantile.Tile(x=0, y=0, z=0)
    ]

    # Antimeridian-crossing bounding boxes are handled
    bounds = (175.0, 5.0, -175.0, 10.0)
    assert len(list(tms.tiles(*bounds, zooms=[2]))) == 2


@pytest.mark.parametrize(
    ("bounds", "expected", "crs", "tms_bbox"),
    [
        # case where east tms bbox crosses antimeridian
        (
            (119.1, -32.86, 119.2, -32.82),
            6,
            32750,
            (100.23646734667152, -79.99407435445299, -158.6052850376368, 0.0),
        ),
        # case where west tms bbox crosses antimeridian
        (
            (11.700978, 52.056474, 11.711114, 52.062706),
            4,
            32632,
            (-17.582877658817317, 0.0, 95.87417095917766, 83.95429547980198),
        ),
    ],
)
def test_tiles_when_tms_bounds_and_provided_bounds_cross_antimeridian(
    bounds: tuple, expected: int, crs: int, tms_bbox: tuple
):
    utm = CRS.from_epsg(crs)
    rs_extent = utm.area_of_use.bounds
    tms = morecantile.TileMatrixSet.custom(
        crs=utm, extent_crs=CRS.from_epsg(4326), extent=list(rs_extent)
    )
    # tms.tiles needs to be aware if tms bounds and input bounds crosses the
    # antimeridian e.g. min(119.2, -158.605) clamps to much larger area. Now
    # that we check to see if lons contain antimeridian, we build tiles that
    # actually overlap the provided bounds to tiles.
    assert tms.bbox == tms_bbox
    for a, b in zip(tms.bbox, tms_bbox):
        assert round(a - b, 6) == 0
    assert len(list(tms.tiles(*bounds, zooms=11))) == expected


def test_tiles_for_tms_with_non_standard_row_col_order():
    """Test tiles from bbox when TMS has non-standard row/col alignment with lat/lon."""
    crs = CRS.from_proj4(
        "+proj=s2 +lat_0=0.0 +lon_0=-90.0 +ellps=WGS84 +UVtoST=quadratic"
    )
    extent = [0.0, 0.0, 1.0, 1.0]
    s2f4 = morecantile.TileMatrixSet.custom(extent, crs, id="S2F4")
    overlapping_tiles = s2f4.tiles(-100, 27, -95, 33, [6])
    assert len(list(overlapping_tiles)) == 30


@pytest.mark.parametrize("identifier", ["WebMercatorQuad", "WebMercatorQuadBottomLeft"])
def test_global_tiles_clamped(identifier):
    """Y is clamped to (0, 2 ** zoom - 1)."""
    tms = morecantile.tms.get(identifier)
    tiles = list(tms.tiles(-180, -90, 180, 90, [1]))
    assert len(tiles) == 4
    assert min(t.y for t in tiles) == 0
    assert max(t.y for t in tiles) == 1


@pytest.mark.parametrize("identifier", ["WebMercatorQuad", "WebMercatorQuadBottomLeft"])
def test_tiles_roundtrip_children(identifier):
    """tiles(bounds(tile)) gives the tile's children"""
    tms = morecantile.tms.get(identifier)
    t = morecantile.Tile(x=3413, y=6202, z=14)
    res = list(tms.tiles(*tms.bounds(t), zooms=[15]))
    assert len(res) == 4


@pytest.mark.parametrize(
    "t",
    [
        morecantile.Tile(x=3413, y=6202, z=14),
        morecantile.Tile(486, 332, 10),
        morecantile.Tile(10, 10, 10),
    ],
)
@pytest.mark.parametrize("identifier", ["WebMercatorQuad", "WebMercatorQuadBottomLeft"])
def test_tiles_roundtrip(t, identifier):
    """Tiles(bounds(tile)) gives the tile."""
    tms = morecantile.tms.get(identifier)
    bounds = tms.bounds(t)
    res = list(tms.tiles(*bounds, zooms=[t.z]))
    assert len(res) == 1
    val = res.pop()
    assert val.x == t.x
    assert val.y == t.y
    assert val.z == t.z


@pytest.mark.parametrize("identifier", ["WebMercatorQuad", "WebMercatorQuadBottomLeft"])
def test_tiles_nan_bounds(identifier):
    """
    nan bounds should raise an error instead of getting clamped to avoid
    unintentionally generating tiles for the entire TMS' extent.
    """
    tms = morecantile.tms.get(identifier)

    bounds = (-105, math.nan, -104.99, 40)
    with pytest.raises(ValueError):
        list(tms.tiles(*bounds, zooms=[14]))


@pytest.mark.parametrize("identifier", ["WebMercatorQuad"])
def test_extend_zoom(identifier):
    """TileMatrixSet.ul should return the correct coordinates."""
    tms = morecantile.tms.get(identifier)
    merc = mercantile.xy_bounds(1000, 1000, 25)
    with pytest.warns(UserWarning):
        more = tms.xy_bounds(1000, 1000, 25)
    for a, b in zip(more, merc):
        assert round(a - b, 6) == 0

    merc = mercantile.xy_bounds(2000, 2000, 26)
    with pytest.warns(UserWarning):
        more = tms.xy_bounds(2000, 2000, 26)
    for a, b in zip(more, merc):
        assert round(a - b, 6) == 0

    merc = mercantile.xy_bounds(2000, 2000, 27)
    with pytest.warns(UserWarning):
        more = tms.xy_bounds(2000, 2000, 27)
    for a, b in zip(more, merc):
        assert round(a - b, 6) == 0

    merc = mercantile.xy_bounds(2000, 2000, 30)
    with pytest.warns(UserWarning):
        more = tms.xy_bounds(2000, 2000, 30)
    for a, b in zip(more, merc):
        assert round(a - b, 6) == 0


def test_is_power_of_two():
    """is power ot 2?"""
    assert is_power_of_two(8)
    assert not is_power_of_two(7)


@pytest.mark.parametrize(
    "t,res",
    [
        (morecantile.Tile(0, 0, 0), True),
        (morecantile.Tile(1, 0, 0), False),
        (morecantile.Tile(0, 0, -1), False),
    ],
)
@pytest.mark.parametrize("identifier", ["WebMercatorQuad", "WebMercatorQuadBottomLeft"])
def test_is_valid_tile(t, res, identifier):
    """test if tile are valid."""
    tms = morecantile.tms.get(identifier)
    assert tms.is_valid(t) == res


@pytest.mark.parametrize("identifier", ["WebMercatorQuad", "WebMercatorQuadBottomLeft"])
def test_neighbors(identifier):
    """test neighbors."""
    tms = morecantile.tms.get(identifier)

    x, y, z = 243, 166, 9
    tiles = tms.neighbors(x, y, z)
    assert len(tiles) == 8
    assert all(t.z == z for t in tiles)
    assert all(t.x - x in (-1, 0, 1) for t in tiles)
    assert all(t.y - y in (-1, 0, 1) for t in tiles)


@pytest.mark.parametrize("identifier", ["WebMercatorQuad", "WebMercatorQuadBottomLeft"])
def test_neighbors_invalid(identifier):
    """test neighbors."""
    tms = morecantile.tms.get(identifier)

    x, y, z = 0, 166, 9
    tiles = tms.neighbors(x, y, z)
    assert len(tiles) == 8 - 3  # no top-left, left, bottom-left
    assert all(t.z == z for t in tiles)
    assert all(t.x - x in (-1, 0, 1) for t in tiles)
    assert all(t.y - y in (-1, 0, 1) for t in tiles)


@pytest.mark.parametrize("identifier", ["WebMercatorQuad", "WebMercatorQuadBottomLeft"])
def test_root_neighbors_invalid(identifier):
    """test neighbors."""
    tms = morecantile.tms.get(identifier)
    x, y, z = 0, 0, 0
    tiles = tms.neighbors(x, y, z)
    assert len(tiles) == 0  # root tile has no neighbors


@pytest.mark.parametrize("identifier", ["WebMercatorQuad", "WebMercatorQuadBottomLeft"])
def test_parent(identifier):
    """test parent"""
    tms = morecantile.tms.get(identifier)
    parent = tms.parent(486, 332, 10)
    assert parent[0] == morecantile.Tile(243, 166, 9)

    with pytest.raises(InvalidZoomError):
        tms.parent(486, 332, 10, zoom=11)

    assert tms.parent(0, 0, 0) == []


@pytest.mark.parametrize("identifier", ["WebMercatorQuad", "WebMercatorQuadBottomLeft"])
def test_parent_multi(identifier):
    """test parent"""
    tms = morecantile.tms.get(identifier)
    parent = tms.parent(486, 332, 10, zoom=8)
    assert parent[0] == morecantile.Tile(121, 83, 8)


@pytest.mark.parametrize("identifier", ["WebMercatorQuad", "WebMercatorQuadBottomLeft"])
def test_children(identifier):
    """test children."""
    tms = morecantile.tms.get(identifier)

    x, y, z = 243, 166, 9
    children = tms.children(x, y, z)
    assert len(children) == 4
    assert morecantile.Tile(2 * x, 2 * y, z + 1) in children
    assert morecantile.Tile(2 * x + 1, 2 * y, z + 1) in children
    assert morecantile.Tile(2 * x + 1, 2 * y + 1, z + 1) in children
    assert morecantile.Tile(2 * x, 2 * y + 1, z + 1) in children


@pytest.mark.parametrize("identifier", ["WebMercatorQuad", "WebMercatorQuadBottomLeft"])
def test_children_multi(identifier):
    """test children multizoom."""
    tms = morecantile.tms.get(identifier)

    children = tms.children(243, 166, 9, zoom=11)
    assert len(children) == 16
    targets = [
        (972, 664, 11),
        (973, 664, 11),
        (973, 665, 11),
        (972, 665, 11),
        (974, 664, 11),
        (975, 664, 11),
        (975, 665, 11),
        (974, 665, 11),
        (974, 666, 11),
        (975, 666, 11),
        (975, 667, 11),
        (974, 667, 11),
        (972, 666, 11),
        (973, 666, 11),
        (973, 667, 11),
        (972, 667, 11),
    ]
    for target in targets:
        assert target in children


@pytest.mark.parametrize("identifier", ["WebMercatorQuad", "WebMercatorQuadBottomLeft"])
def test_children_invalid_zoom(identifier):
    """invalid zoom."""
    tms = morecantile.tms.get(identifier)
    with pytest.raises(InvalidZoomError):
        tms.children(243, 166, 9, zoom=8)

    with pytest.raises(InvalidZoomError):
        tms.children((243, 166, 9), zoom=8)
