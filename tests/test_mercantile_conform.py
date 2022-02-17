"""Test Conformance with Mercantile."""

from random import sample

import mercantile
import pytest

import morecantile

tms = morecantile.tms.get("WebMercatorQuad")


@pytest.mark.parametrize("zoom", range(0, 20))
def test_get_tile(zoom: int):
    """Make sure mercantile and morecantile returns the same thing."""
    tile = mercantile.tile(0, 0, zoom=zoom)
    morecantile_tile = tms.tile(0, 0, zoom=zoom)
    assert tile == morecantile_tile


@pytest.mark.parametrize("zoom", range(0, 20))
def test_bounds(zoom: int):
    """Make sure mercantile and morecantile returns the same thing."""
    # get random x,y index
    x = sample(range(0, tms.matrix(zoom).matrixWidth), 1)[0]
    y = sample(range(0, tms.matrix(zoom).matrixHeight), 1)[0]

    for a, b in zip(
        mercantile.xy_bounds(x, y, zoom), tms.xy_bounds(morecantile.Tile(x, y, zoom))
    ):
        assert round(a - b, 7) == 0
