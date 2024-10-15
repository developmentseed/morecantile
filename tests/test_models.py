"""Test TileMatrixSet model."""

import json
import os
import random
from collections.abc import Iterable

import pyproj
import pytest
from pydantic import ValidationError
from rasterio.crs import CRS as rioCRS

import morecantile
from morecantile.commons import Tile
from morecantile.errors import InvalidIdentifier
from morecantile.models import CRS, CRSWKT, CRSUri, TileMatrix, TileMatrixSet

data_dir = os.path.join(os.path.dirname(__file__), "../morecantile/data")
tilesets = [
    os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith(".json")
]
tms_v1_dir = os.path.join(os.path.dirname(__file__), "fixtures", "v1_tms")


@pytest.mark.parametrize("tileset", tilesets)
def test_tile_matrix_set(tileset):
    """Load TileMatrixSet in models."""
    # Confirm model validation is working
    with open(tileset, "r") as f:
        ts = TileMatrixSet.model_validate_json(f.read())
    # This would fail if `crs` isn't supported by PROJ
    assert isinstance(ts.crs._pyproj_crs, pyproj.CRS)
    assert isinstance(ts.geographic_crs, pyproj.CRS)
    assert repr(ts)


@pytest.mark.parametrize("tileset", tilesets)
def test_geographic_crs_bbox(tileset):
    """check that geographic bounds are correct."""
    with open(tileset, "r") as f:
        ts = TileMatrixSet.model_validate_json(f.read())

    if not pyproj.CRS.from_epsg(4326) == ts.geographic_crs:
        _to_geographic = pyproj.Transformer.from_crs(
            ts.crs._pyproj_crs, pyproj.CRS.from_epsg(4326), always_xy=True
        )
        bbox = _to_geographic.transform_bounds(*ts.xy_bbox, densify_pts=21)
        assert bbox == ts.bbox


def test_tile_matrix_iter():
    """Test iterator"""
    tms = morecantile.tms.get("WebMercatorQuad")
    assert isinstance(tms, Iterable)
    for matrix in tms:
        assert isinstance(matrix, TileMatrix)


def test_tile_matrix_order():
    """Test matrix order"""
    tms = morecantile.tms.get("WebMercatorQuad")
    matrices = tms.tileMatrices[:]
    random.shuffle(matrices)
    tms_ordered = TileMatrixSet(
        title=tms.title,
        id=tms.id,
        crs=tms.crs,
        tileMatrices=matrices,
    )
    # Confirm sort
    assert [matrix.id for matrix in tms.tileMatrices] == [
        matrix.id for matrix in tms_ordered.tileMatrices
    ]

    # Confirm sort direction
    assert int(tms_ordered.tileMatrices[-1].id) > int(tms_ordered.tileMatrices[0].id)


def test_invalid_tms():
    """should raise an error when tms name is not found."""
    with pytest.raises(InvalidIdentifier):
        morecantile.tms.get("ANotValidName")


@pytest.mark.parametrize(
    "name,result",
    [
        ("LINZAntarticaMapTilegrid", False),
        ("EuropeanETRS89_LAEAQuad", True),
        ("CanadianNAD83_LCC", False),
        ("UPSArcticWGS84Quad", True),
        ("NZTM2000Quad", True),
        ("UTM31WGS84Quad", False),
        ("UPSAntarcticWGS84Quad", True),
        ("WorldMercatorWGS84Quad", True),
        ("WGS1984Quad", False),
        ("WorldCRS84Quad", False),
        ("WebMercatorQuad", True),
        ("CDB1GlobalGrid", False),
        ("GNOSISGlobalGrid", False),
    ],
)
def test_quadkey_support(name, result):
    """test for Quadkey support."""
    tms = morecantile.tms.get(name)
    assert tms.is_quadtree == result


def test_quadkey():
    """Test tile to quadkey."""
    tms = morecantile.tms.get("WebMercatorQuad")
    expected = "0313102310"
    assert tms.quadkey(486, 332, 10) == expected


def test_quadkey_to_tile():
    """Test quadkey to tile."""
    tms = morecantile.tms.get("WebMercatorQuad")
    qk = "0313102310"
    expected = Tile(486, 332, 10)
    assert tms.quadkey_to_tile(qk) == expected


def test_empty_quadkey_to_tile():
    """Empty qk should give tile 0,0,0."""
    tms = morecantile.tms.get("WebMercatorQuad")
    qk = ""
    expected = Tile(0, 0, 0)
    assert tms.quadkey_to_tile(qk) == expected


def test_quadkey_failure():
    """makde sure we don't support stupid quadkeys."""
    tms = morecantile.tms.get("WebMercatorQuad")
    with pytest.raises(morecantile.errors.QuadKeyError):
        tms.quadkey_to_tile("lolwut")


def test_findMatrix():
    """Should raise an error when TileMatrix is not found."""
    tms = morecantile.tms.get("WebMercatorQuad")
    m = tms.matrix(0)
    assert m.id == "0"

    with pytest.warns(UserWarning):
        tms.matrix(26)


def test_Custom():
    """Create custom TMS grid."""
    tms = morecantile.tms.get("WebMercatorQuad")

    # Web Mercator Extent
    extent = (-20037508.3427892, -20037508.3427892, 20037508.3427892, 20037508.3427892)
    custom_tms = TileMatrixSet.custom(extent, pyproj.CRS.from_epsg(3857))

    assert tms.tile(20.0, 15.0, 5) == custom_tms.tile(20.0, 15.0, 5)

    wmMat = tms.matrix(5)
    cusMat = custom_tms.matrix(5)
    assert wmMat.matrixWidth == cusMat.matrixWidth
    assert wmMat.matrixHeight == cusMat.matrixHeight
    assert round(wmMat.scaleDenominator, 6) == round(cusMat.scaleDenominator, 6)
    assert round(wmMat.pointOfOrigin[0], 6) == round(cusMat.pointOfOrigin[0], 6)

    extent = (-180.0, -85.051128779806, 180.0, 85.051128779806)
    custom_tms = TileMatrixSet.custom(
        extent, pyproj.CRS.from_epsg(3857), extent_crs=pyproj.CRS.from_epsg(4326)
    )

    assert tms.tile(20.0, 15.0, 5) == custom_tms.tile(20.0, 15.0, 5)

    wmMat = tms.matrix(5)
    cusMat = custom_tms.matrix(5)
    assert wmMat.matrixWidth == cusMat.matrixWidth
    assert wmMat.matrixHeight == cusMat.matrixHeight
    assert round(wmMat.scaleDenominator, 6) == round(cusMat.scaleDenominator, 6)
    assert round(wmMat.pointOfOrigin[0], 6) == round(cusMat.pointOfOrigin[0], 6)

    extent = (-20037508.3427892, -20037508.3427892, 20037508.3427892, 20037508.3427892)
    custom_tms = TileMatrixSet.custom(extent, pyproj.CRS.from_epsg(3857))
    assert isinstance(custom_tms.geographic_crs, pyproj.CRS)
    assert custom_tms.geographic_crs == pyproj.CRS.from_epsg(4326)

    extent = (-20037508.3427892, -20037508.3427892, 20037508.3427892, 20037508.3427892)
    custom_tms = TileMatrixSet.custom(extent, pyproj.CRS.from_epsg(3857))
    assert isinstance(custom_tms.geographic_crs, pyproj.CRS)


def test_custom_tms_bounds_epsg4326():
    """Check bounds with epsg4326."""
    custom_tms = TileMatrixSet.custom((-120, 30, -110, 40), pyproj.CRS.from_epsg(4326))
    assert custom_tms.xy_bbox == (-120, 30, -110, 40)
    assert custom_tms.bbox == (-120, 30, -110, 40)
    assert custom_tms.xy_bounds(0, 0, 0) == (-120, 30, -110, 40)
    assert custom_tms.bounds(0, 0, 0) == (-120, 30, -110, 40)


# When using `from_user_input`, `morecantile.models.crs_axis_inverted` should return the valid result.
def test_custom_tms_bounds_user_crs():
    """Check bounds with epsg4326."""
    custom_tms = TileMatrixSet.custom(
        (-120, 30, -110, 40),
        pyproj.CRS.from_epsg(4326),
    )
    assert custom_tms.xy_bbox == (-120, 30, -110, 40)
    assert custom_tms.bbox == (-120, 30, -110, 40)
    assert custom_tms.xy_bounds(0, 0, 0) == (-120, 30, -110, 40)
    assert custom_tms.bounds(0, 0, 0) == (-120, 30, -110, 40)


def test_custom_tms_decimation():
    """Check bounds with epsg6342 and custom decimation base."""
    extent = (238170, 4334121, 377264, 4473215)
    left, bottom, right, top = extent
    for decimation_base in [2, 3, 4, 5]:
        custom_tms = TileMatrixSet.custom(
            extent,
            pyproj.CRS.from_epsg(6342),
            decimation_base=decimation_base,
        )

        if decimation_base == 2:
            assert custom_tms.is_quadtree
        else:
            assert not custom_tms.is_quadtree

        for zoom in [0, 1, 2, 3]:
            tile_width = (right - left) / decimation_base**zoom
            tile_height = (top - bottom) / decimation_base**zoom
            expected = (left, top - tile_height, left + tile_width, top)
            tile_bounds = custom_tms.xy_bounds(0, 0, zoom)
            for a, b in zip(expected, tile_bounds):
                assert round(a - b, 4) == 0


def test_nztm_quad_is_quad():
    """Test NZTM2000Quad."""
    tms = morecantile.tms.get("NZTM2000Quad")
    bound = tms.xy_bounds(morecantile.Tile(0, 0, 0))
    expected = (-3260586.7284, 419435.9938, 6758167.443, 10438190.1652)
    for a, b in zip(expected, bound):
        assert round(a - b, 4) == 0


# NZTM2000Quad should use all the WebMercatorQuad zoom scales
def test_nztm_quad_scales():
    """Test NZTM2000Quad."""
    nztm_tms = morecantile.tms.get("NZTM2000Quad")
    google_tms = morecantile.tms.get("WebMercatorQuad")
    for z in range(2, nztm_tms.maxzoom + 2):
        assert (
            round(
                google_tms.matrix(z).scaleDenominator
                - nztm_tms.matrix(z - 2).scaleDenominator,
                4,
            )
            == 0
        )


def test_InvertedLatLonGrids():
    """Check Inverted LatLon grids."""

    tms = morecantile.tms.get("LINZAntarticaMapTilegrid")
    assert tms.xy_bbox == (
        -918457.73,
        -22441670.269999996,
        28441670.269999996,
        6918457.73,
    )


def test_zoom_for_res():
    """Get TMS zoom level corresponding to a specific resolution."""
    tms = morecantile.tms.get("WebMercatorQuad")

    # native resolution of zoom 7 is 1222.9924525628178
    # native resolution of zoom 8 is 611.4962262814075
    assert tms.zoom_for_res(612.0) == 8
    assert tms.zoom_for_res(612.0, zoom_level_strategy="lower") == 7
    assert tms.zoom_for_res(612.0, zoom_level_strategy="upper") == 8

    assert tms.zoom_for_res(610.0) == 8

    # native resolution of zoom 24 is 0.009330691929342784
    assert tms.zoom_for_res(0.0001) == 24

    # theoritical resolution of zoom 25 is 0.004665345964671392
    with pytest.warns(UserWarning):
        assert tms.zoom_for_res(0.0001, max_z=25) == 25

    # minzoom greater than 0
    crs = pyproj.CRS.from_epsg(3857)
    extent = [-20026376.39, -20048966.10, 20026376.39, 20048966.10]
    tms = morecantile.TileMatrixSet.custom(
        extent, crs, id="MyCustomTmsEPSG3857", minzoom=6
    )
    assert tms.zoom_for_res(10) == 14
    assert tms.zoom_for_res(5000) == 6


def test_schema():
    """Translate Model to Schema."""
    tms = morecantile.tms.get("WebMercatorQuad")
    assert tms.model_json_schema()
    assert tms.model_dump_json(exclude_none=True)
    assert tms.model_dump(exclude_none=True)

    crs = pyproj.CRS.from_proj4(
        "+proj=stere +lat_0=90 +lon_0=0 +k=2 +x_0=0 +y_0=0 +R=3396190 +units=m +no_defs"
    )
    extent = [-13584760.000, -13585240.000, 13585240.000, 13584760.000]
    tms = morecantile.TileMatrixSet.custom(extent, crs, id="MarsNPolek2MOLA5k")
    assert tms.model_json_schema()
    assert tms.model_dump(exclude_none=True)
    json_doc = json.loads(tms.model_dump_json(exclude_none=True))
    assert json_doc["crs"] == "http://www.opengis.net/def/crs/IAU/2015/49930"

    crs = pyproj.CRS.from_epsg(3031)
    extent = [-948.75, -543592.47, 5817.41, -3333128.95]  # From https:///epsg.io/3031
    tms = morecantile.TileMatrixSet.custom(extent, crs, id="MyCustomTmsEPSG3031")
    assert tms.model_json_schema()
    assert tms.model_dump_json(exclude_none=True)
    json_doc = json.loads(tms.model_dump_json(exclude_none=True))
    assert json_doc["crs"] == "http://www.opengis.net/def/crs/EPSG/0/3031"


def test_mars_tms():
    """The Mars global mercator scheme should broadly align with the Earth
    Web Mercator CRS, despite the different planetary radius and scale.
    """
    MARS2000_SPHERE = pyproj.CRS.from_proj4("+proj=longlat +R=3396190 +no_defs")

    MARS_MERCATOR = pyproj.CRS.from_proj4(
        "+proj=merc +R=3396190 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +no_defs"
    )

    # same boundaries as Earth mercator
    mars_tms = TileMatrixSet.custom(
        [
            -179.9999999999996,
            -85.05112877980656,
            179.9999999999996,
            85.05112877980656,
        ],
        MARS_MERCATOR,
        extent_crs=MARS2000_SPHERE,
        title="Web Mercator Mars",
    )
    assert mars_tms.geographic_crs == MARS2000_SPHERE

    pos = (35, 40, 3)
    mars_tile = mars_tms.tile(*pos)
    mercator_tms = morecantile.tms.get("WebMercatorQuad")
    earth_tile = mercator_tms.tile(*pos)

    assert mars_tile.x == earth_tile.x
    assert mars_tile.y == earth_tile.y
    assert mars_tile.z == earth_tile.z == 3

    _to_geographic = pyproj.Transformer.from_crs(
        mars_tms.crs._pyproj_crs, MARS2000_SPHERE, always_xy=True
    )
    bbox = _to_geographic.transform_bounds(*mars_tms.xy_bbox, densify_pts=21)
    assert bbox == mars_tms.bbox


def test_mars_local_tms():
    """Local TMS using Mars CRS"""
    MARS2000_SPHERE = pyproj.CRS.from_proj4("+proj=longlat +R=3396190 +no_defs")

    # A transverse mercator projection for the landing site of the Perseverance rover.
    SYRTIS_TM = pyproj.CRS.from_proj4(
        "+proj=tmerc +lat_0=17 +lon_0=76.5 +k=0.9996 +x_0=0 +y_0=0 +a=3396190 +b=3376200 +units=m +no_defs"
    )
    # 100km grid centered on 17N, 76.5E
    syrtis_tms = TileMatrixSet.custom(
        [-5e5, -5e5, 5e5, 5e5],
        SYRTIS_TM,
        title="Web Mercator Mars",
    )
    assert SYRTIS_TM == syrtis_tms.crs._pyproj_crs
    assert syrtis_tms.geographic_crs
    assert syrtis_tms.model_dump(mode="json")

    center = syrtis_tms.ul(1, 1, 1)
    assert round(center.x, 6) == 76.5
    assert round(center.y, 6) == 17

    _to_geographic = pyproj.Transformer.from_crs(
        syrtis_tms.crs._pyproj_crs, MARS2000_SPHERE, always_xy=True
    )
    bbox = _to_geographic.transform_bounds(*syrtis_tms.xy_bbox, densify_pts=21)
    assert bbox == syrtis_tms.bbox


def test_mars_tms_construction():
    mars_sphere_crs = pyproj.CRS.from_user_input("IAU_2015:49900")
    extent = [-180.0, -90.0, 180.0, 90.0]
    mars_tms = morecantile.TileMatrixSet.custom(
        extent,
        crs=mars_sphere_crs,
        id="MarsGeographicCRS",
        matrix_scale=[2, 1],
    )
    assert "4326" not in mars_tms.geographic_crs.to_wkt()
    assert "4326" not in mars_tms.rasterio_geographic_crs.to_wkt()
    assert mars_tms.xy_bbox.left == pytest.approx(-180.0)
    assert mars_tms.xy_bbox.bottom == pytest.approx(-90.0)
    assert mars_tms.xy_bbox.right == pytest.approx(180.0)
    assert mars_tms.xy_bbox.top == pytest.approx(90.0)


def test_mars_web_mercator_long_lat():
    mars_sphere_crs = pyproj.CRS.from_user_input("IAU_2015:49900")
    wkt_mars_web_mercator = 'PROJCRS["Mars (2015) - Sphere XY / Pseudo-Mercator",BASEGEOGCRS["Mars (2015) - Sphere",DATUM["Mars (2015) - Sphere",ELLIPSOID["Mars (2015) - Sphere",3396190,0,LENGTHUNIT["metre",1,ID["EPSG",9001]]],ANCHOR["Viking 1 lander : 47.95137 W"]],PRIMEM["Reference Meridian",0,ANGLEUNIT["degree",0.0174532925199433,ID["EPSG",9122]]]],CONVERSION["Popular Visualisation Pseudo-Mercator",METHOD["Popular Visualisation Pseudo Mercator",ID["EPSG",1024]],PARAMETER["Latitude of natural origin",0,ANGLEUNIT["degree",0.0174532925199433],ID["EPSG",8801]],PARAMETER["Longitude of natural origin",0,ANGLEUNIT["degree",0.0174532925199433],ID["EPSG",8802]],PARAMETER["False easting",0,LENGTHUNIT["metre",1],ID["EPSG",8806]],PARAMETER["False northing",0,LENGTHUNIT["metre",1],ID["EPSG",8807]]],CS[Cartesian,2],AXIS["easting (X)",east,ORDER[1],LENGTHUNIT["metre",1,ID["EPSG",9001]]],AXIS["northing (Y)",north,ORDER[2],LENGTHUNIT["metre",1,ID["EPSG",9001]]],USAGE[SCOPE["Web mapping and visualisation."],AREA["World between 85.06 S and 85.06 N."],BBOX[-85.850511287,-180,85.0511287,180]],REMARK["Use semi-major radius as sphere radius for interoperability. Source of IAU Coordinate systems: doi:10.1007/s10569-017-9805-5"]]'
    crs_mars_web_mercator = pyproj.CRS.from_wkt(wkt_mars_web_mercator)
    extent_wm = [-180.0, -85.850511287, 180.0, 85.850511287]
    mars_tms_wm = morecantile.TileMatrixSet.custom(
        extent_wm,
        extent_crs=mars_sphere_crs,
        crs=crs_mars_web_mercator,
        id="MarsWebMercator",
    )
    assert "4326" not in mars_tms_wm.geographic_crs.to_wkt()
    assert "4326" not in mars_tms_wm.rasterio_geographic_crs.to_wkt()
    assert mars_tms_wm.bbox.left == pytest.approx(-180.0)
    assert mars_tms_wm.bbox.bottom == pytest.approx(-85.850511287)
    assert mars_tms_wm.bbox.right == pytest.approx(180.0)
    assert mars_tms_wm.bbox.top == pytest.approx(85.850511287)


@pytest.mark.parametrize(
    "identifier, file, crs",
    [
        (
            "UPSAntarcticWGS84Quad",
            os.path.join(tms_v1_dir, "UPSAntarcticWGS84Quad.json"),
            5042,
        ),
        ("CanadianNAD83_LCC", os.path.join(tms_v1_dir, "CanadianNAD83_LCC.json"), 3978),
        ("WebMercatorQuad", os.path.join(tms_v1_dir, "WebMercatorQuad.json"), 3857),
    ],
)
def test_from_v1(identifier, file, crs):
    """
    Test from_v1 class method
    """
    with open(file) as fp:
        v1_tms = json.load(fp)

    tms = TileMatrixSet.from_v1(v1_tms)
    assert tms.id == identifier
    assert tms.crs._pyproj_crs == pyproj.CRS.from_epsg(crs)


@pytest.mark.parametrize(
    "id,result",
    [
        ("LINZAntarticaMapTilegrid", True),
        ("EuropeanETRS89_LAEAQuad", True),
        ("CanadianNAD83_LCC", False),
        ("UPSArcticWGS84Quad", False),
        ("NZTM2000Quad", True),
        ("UTM31WGS84Quad", False),
        ("UPSAntarcticWGS84Quad", False),
        ("WorldMercatorWGS84Quad", False),
        ("WorldCRS84Quad", False),
        ("WGS1984Quad", True),
        ("WebMercatorQuad", False),
        ("CDB1GlobalGrid", True),
        ("GNOSISGlobalGrid", True),
    ],
)
def test_inverted_tms(id, result):
    """Make sure _invert_axis return the correct result."""
    assert morecantile.tms.get(id)._invert_axis == result


@pytest.mark.parametrize(
    "id,result",
    [
        ("LINZAntarticaMapTilegrid", False),
        ("EuropeanETRS89_LAEAQuad", False),
        ("CanadianNAD83_LCC", False),
        ("UPSArcticWGS84Quad", False),
        ("NZTM2000Quad", False),
        ("UTM31WGS84Quad", False),
        ("UPSAntarcticWGS84Quad", False),
        ("WorldMercatorWGS84Quad", False),
        ("WorldCRS84Quad", False),
        ("WGS1984Quad", False),
        ("WebMercatorQuad", False),
        ("CDB1GlobalGrid", True),
        ("GNOSISGlobalGrid", True),
    ],
)
def test_variable_tms(id, result):
    """Make sure is_variable return the correct result."""
    assert morecantile.tms.get(id).is_variable == result


@pytest.mark.parametrize(
    "authority,code,result",
    [
        ("EPSG", "4326", "EPSG/0/4326"),
        ("ESRI", "102001", "ESRI/0/102001"),
        ("IAU_2015", "49910", "IAU/2015/49910"),
        ("IGNF", "AMANU49", "IGNF/0/AMANU49"),
        ("NKG", "ETRF00", "NKG/0/ETRF00"),
        ("OGC", "CRS84", "OGC/0/CRS84"),
    ],
)
def test_crs_uris(authority, code, result):
    """Test CRS URIS."""
    assert (
        morecantile.models.CRS_to_uri(pyproj.CRS((authority, code)))
        == f"http://www.opengis.net/def/crs/{result}"
    )


@pytest.mark.parametrize("tilematrixset", morecantile.tms.list())
def test_crs_uris_for_defaults(tilematrixset):
    """Test CRS URIS."""
    t = morecantile.tms.get(tilematrixset)
    assert t.crs._pyproj_crs == morecantile.models.CRS_to_uri(t.crs._pyproj_crs)


def test_rasterio_crs():
    """Check rasterio CRS methods."""
    tms = morecantile.tms.get("WebMercatorQuad")
    assert isinstance(tms.rasterio_crs, rioCRS)
    assert isinstance(tms.rasterio_geographic_crs, rioCRS)
    assert tms.rasterio_crs == rioCRS.from_epsg(3857)
    assert tms.rasterio_geographic_crs == rioCRS.from_epsg(4326)

    tms = morecantile.tms.get("WGS1984Quad")
    assert tms.rasterio_crs == rioCRS.from_epsg(4326)
    assert tms.rasterio_geographic_crs == rioCRS.from_epsg(4326)


def test_boundingbox():
    """Test boundingbox support."""
    with pytest.raises(ValidationError):
        TileMatrixSet(
            **{
                "crs": "http://www.opengis.net/def/crs/EPSG/0/3857",
                "boundingBox": {
                    "lowerLeft": [],
                    "upperRight": [],
                    "crs": "http://www.opengis.net/def/crs/EPSG/0/3857",
                    "orderedAxes": ["X", "Y"],
                },
                "tileMatrices": [
                    {
                        "id": "0",
                        "scaleDenominator": 559082264.028717,
                        "cellSize": 156543.033928041,
                        "pointOfOrigin": [-20037508.342789244, 20037508.342789244],
                        "tileWidth": 256,
                        "tileHeight": 256,
                        "matrixWidth": 1,
                        "matrixHeight": 1,
                    },
                ],
            }
        )

    assert TileMatrixSet(
        **{
            "crs": "http://www.opengis.net/def/crs/EPSG/0/3857",
            "boundingBox": {
                "lowerLeft": [-20037508.342789244, -20037508.34278919],
                "upperRight": [20037508.34278919, 20037508.342789244],
            },
            "tileMatrices": [
                {
                    "id": "0",
                    "scaleDenominator": 559082264.028717,
                    "cellSize": 156543.033928041,
                    "pointOfOrigin": [-20037508.342789244, 20037508.342789244],
                    "tileWidth": 256,
                    "tileHeight": 256,
                    "matrixWidth": 1,
                    "matrixHeight": 1,
                },
            ],
        }
    )

    assert TileMatrixSet(
        **{
            "crs": "http://www.opengis.net/def/crs/EPSG/0/3857",
            "boundingBox": {
                "lowerLeft": [-20037508.342789244, -20037508.34278919],
                "upperRight": [20037508.34278919, 20037508.342789244],
                "crs": "http://www.opengis.net/def/crs/EPSG/0/3857",
                "orderedAxes": ["X", "Y"],
            },
            "tileMatrices": [
                {
                    "id": "0",
                    "scaleDenominator": 559082264.028717,
                    "cellSize": 156543.033928041,
                    "pointOfOrigin": [-20037508.342789244, 20037508.342789244],
                    "tileWidth": 256,
                    "tileHeight": 256,
                    "matrixWidth": 1,
                    "matrixHeight": 1,
                },
            ],
        }
    )


def test_private_attr():
    """Check private attr."""
    tms = morecantile.tms.get("WebMercatorQuad")
    assert "_to_geographic" in tms.__private_attributes__
    assert "_from_geographic" in tms.__private_attributes__


def test_crs_type():
    """Test CRSType Model."""
    uri = "http://www.opengis.net/def/crs/EPSG/0/3857"
    crs = CRS(uri)
    assert crs.root == uri
    assert crs.model_dump() == uri
    # PROJ methods
    assert crs._pyproj_crs == pyproj.CRS.from_epsg(3857)
    assert crs.srs == "http://www.opengis.net/def/crs/EPSG/0/3857"
    assert crs.to_epsg() == 3857
    assert crs.to_wkt() == pyproj.CRS.from_epsg(3857).to_wkt()
    assert crs.to_proj4() == pyproj.CRS.from_epsg(3857).to_proj4()
    assert crs.to_dict() == pyproj.CRS.from_epsg(3857).to_dict()
    assert crs.to_json() == pyproj.CRS.from_epsg(3857).to_json()

    # with Options
    assert crs.to_epsg(min_confidence=10) == 3857
    assert crs.to_wkt(pretty=True) == pyproj.CRS.from_epsg(3857).to_wkt(pretty=True)
    assert crs.to_proj4(5) == pyproj.CRS.from_epsg(3857).to_proj4(5)
    assert crs.to_json(pretty=True) == pyproj.CRS.from_epsg(3857).to_json(pretty=True)

    # Outside OGC Specs but it works
    wkt = pyproj.CRS.from_epsg(3857).to_wkt()
    crs = CRS(wkt)
    assert crs.root == wkt
    assert crs.model_dump() == wkt
    # PROJ methods
    assert crs._pyproj_crs == pyproj.CRS.from_epsg(3857)
    assert crs.srs == wkt
    assert crs.to_epsg() == 3857

    # CRSUri
    data = {"uri": "http://www.opengis.net/def/crs/EPSG/0/3857"}
    crs = CRS(data)
    assert crs.root == CRSUri(uri="http://www.opengis.net/def/crs/EPSG/0/3857")
    assert (
        crs.model_dump(mode="json") == data
    )  # we use `mode=json` to dump all sub-model (URL)
    assert crs._pyproj_crs == pyproj.CRS.from_epsg(3857)

    # CRSWKT
    wkt = pyproj.CRS.from_epsg(3857).to_json_dict()
    crs = CRS({"wkt": wkt})
    assert crs.root == CRSWKT(wkt=wkt)
    assert crs.model_dump()["wkt"] == wkt
    assert crs._pyproj_crs == pyproj.CRS.from_epsg(3857)

    # CRSRef
    with pytest.raises(NotImplementedError):
        CRS({"referenceSystem": {"yo": 1}})

    # something else
    with pytest.raises(ValidationError):
        CRS({"Hey": 1})


def test_crs_type_in_tms():
    """Check TMS representation when using non-string CRS."""
    # CRS URI
    crs = {"uri": "http://www.opengis.net/def/crs/EPSG/0/3857"}
    tms = TileMatrixSet(
        **{
            "crs": crs,
            "boundingBox": {
                "lowerLeft": [-20037508.342789244, -20037508.34278919],
                "upperRight": [20037508.34278919, 20037508.342789244],
            },
            "tileMatrices": [
                {
                    "id": "0",
                    "scaleDenominator": 559082264.028717,
                    "cellSize": 156543.033928041,
                    "pointOfOrigin": [-20037508.342789244, 20037508.342789244],
                    "tileWidth": 256,
                    "tileHeight": 256,
                    "matrixWidth": 1,
                    "matrixHeight": 1,
                },
            ],
        }
    )
    assert str(tms.crs.root.uri) == "http://www.opengis.net/def/crs/EPSG/0/3857"
    assert repr(tms)
