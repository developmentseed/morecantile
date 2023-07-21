"""Tests for morecantile."""

import pytest

import morecantile
from morecantile.commons import BoundingBox, Tile
from morecantile.errors import InvalidZoomError
from morecantile.models import TileMatrix

gnosisg_tms = morecantile.tms.get("GNOSISGlobalGrid")
cdb1_tms = morecantile.tms.get("CDB1GlobalGrid")


def test_coalesce():
    """test get coalesce."""
    matrix = TileMatrix(
        **{
            "id": "2",
            "scaleDenominator": 34942641.501794859767,
            "cellSize": 0.087890625,
            "cornerOfOrigin": "topLeft",
            "pointOfOrigin": [90, -180],
            "matrixWidth": 16,
            "matrixHeight": 8,
            "tileWidth": 256,
            "tileHeight": 256,
            "variableMatrixWidths": [
                {"coalesce": 4, "minTileRow": 0, "maxTileRow": 0},
                {"coalesce": 2, "minTileRow": 1, "maxTileRow": 1},
                {"coalesce": 2, "minTileRow": 6, "maxTileRow": 6},
                {"coalesce": 4, "minTileRow": 7, "maxTileRow": 7},
            ],
        }
    )

    assert matrix.get_coalesce_factor(0) == 4
    assert matrix.get_coalesce_factor(1) == 2
    assert matrix.get_coalesce_factor(3) == 1
    assert matrix.get_coalesce_factor(6) == 2
    assert matrix.get_coalesce_factor(7) == 4

    with pytest.raises(ValueError):
        matrix.get_coalesce_factor(8)

    with pytest.raises(ValueError):
        matrix.get_coalesce_factor(-1)

    matrix = TileMatrix(
        **{
            "id": "2",
            "scaleDenominator": 34942641.501794859767,
            "cellSize": 0.087890625,
            "cornerOfOrigin": "topLeft",
            "pointOfOrigin": [90, -180],
            "matrixWidth": 16,
            "matrixHeight": 8,
            "tileWidth": 256,
            "tileHeight": 256,
        }
    )
    with pytest.raises(ValueError):
        matrix.get_coalesce_factor(0)


def test_invalid_matrix():
    """Should raise error because we cannot construct a Matrix for variableWidth TMS."""
    with pytest.raises(InvalidZoomError):
        cdb1_tms.matrix(22)

    with pytest.raises(InvalidZoomError):
        gnosisg_tms.matrix(29)


def test_gnosisg():
    """test GNOSISGlobalGrid TMS."""
    bounds = gnosisg_tms.xy_bounds(0, 0, 0)
    assert bounds == BoundingBox(-180, 0, -90, 90)

    bounds = gnosisg_tms.xy_bounds(1, 1, 0)
    assert bounds == BoundingBox(-90, -90, 0, 0)

    bounds = gnosisg_tms.xy_bounds(0, 0, 1)
    assert bounds == BoundingBox(-180, 45, -90, 90)

    # tile for index 0,0 and 1,0 should have the same bounds
    assert gnosisg_tms.xy_bounds(0, 0, 1) == gnosisg_tms.xy_bounds(1, 0, 1)
    assert gnosisg_tms.xy_bounds(2, 0, 1) == gnosisg_tms.xy_bounds(3, 0, 1)
    assert gnosisg_tms.xy_bounds(4, 0, 1) == gnosisg_tms.xy_bounds(5, 0, 1)
    assert gnosisg_tms.xy_bounds(6, 0, 1) == gnosisg_tms.xy_bounds(7, 0, 1)

    assert gnosisg_tms.xy_bounds(0, 1, 1) != gnosisg_tms.xy_bounds(1, 1, 1)
    assert gnosisg_tms.xy_bounds(2, 1, 1) != gnosisg_tms.xy_bounds(3, 1, 1)

    assert gnosisg_tms.xy_bounds(0, 3, 1) == gnosisg_tms.xy_bounds(1, 3, 1)
    assert gnosisg_tms.xy_bounds(2, 3, 1) == gnosisg_tms.xy_bounds(3, 3, 1)
    assert gnosisg_tms.xy_bounds(4, 3, 1) == gnosisg_tms.xy_bounds(5, 3, 1)
    assert gnosisg_tms.xy_bounds(6, 3, 1) == gnosisg_tms.xy_bounds(7, 3, 1)

    # crs and geographic crs are the same
    assert gnosisg_tms.xy_bounds(0, 0, 0) == gnosisg_tms.bounds(0, 0, 0)
    assert gnosisg_tms.xy_bounds(1, 1, 0) == gnosisg_tms.bounds(1, 1, 0)
    assert gnosisg_tms.xy_bounds(0, 0, 1) == gnosisg_tms.bounds(0, 0, 1)

    tiles = gnosisg_tms.tiles(-180, -90, 180, 90, [0])
    assert len(list(tiles)) == 8

    tiles = gnosisg_tms.tiles(-180, -90, 180, 90, [1])
    assert len(list(tiles)) == 32

    assert len(gnosisg_tms.parent(Tile(0, 0, 1))) == 1
    assert len(gnosisg_tms.parent(Tile(0, 0, 2))) == 2
    assert len(gnosisg_tms.parent(Tile(0, 0, 3))) == 4

    assert len(gnosisg_tms.children(Tile(0, 0, 0), zoom=1)) == 4
