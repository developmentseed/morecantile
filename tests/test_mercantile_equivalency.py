import mercantile
import pytest

import morecantile

tms = morecantile.tms.get("WebMercatorQuad")


@pytest.mark.parametrize("zoom", range(0, 20))
def test_get_tile(zoom: int):
    tile = mercantile.tile(0, 0, zoom=zoom)
    morecantile_tile = tms.tile(0, 0, zoom=zoom)
    assert tile == morecantile_tile
