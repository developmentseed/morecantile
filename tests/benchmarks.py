"""Morecantile benchmark."""

import pytest

import morecantile
from morecantile.commons import BoundingBox

tms = morecantile.tms.get("WebMercatorQuad")

# Test tiles from https://github.com/jessekrubin/utiles/blob/ea58b9a017a2e3528f03cc20f16ef531737b863f/utiles-pyo3/bench/test_bench.py
TEST_TILES = (
    (0, 0, 0),
    (1, 0, 1),
    (1, 1, 1),
    (1, 40, 7),
    (486, 332, 10),
    # HIGH ZOOM
    (486, 332, 20),
    # OUTSIDE TMS Range
    (486, 332, 30),
)


@pytest.mark.parametrize("tile", TEST_TILES)
def test_bounds(tile, benchmark):
    str_tile = "Tile(x={},y={},z={})".format(*tile)
    benchmark.name = f"morecantile.bounds-{str_tile}"
    benchmark.fullname = f"morecantile.bounds-{str_tile}"
    benchmark.group = "morecantile.bounds"

    r = benchmark(tms.bounds, *tile)
    assert isinstance(r, BoundingBox)


@pytest.mark.parametrize("tile", TEST_TILES)
def test_xy_bounds(tile, benchmark) -> None:
    str_tile = "Tile(x={},y={},z={})".format(*tile)
    benchmark.name = f"morecantile.xy_bounds-{str_tile}"
    benchmark.fullname = f"morecantile.xy_bounds-{str_tile}"
    benchmark.group = "morecantile.xy_bounds"

    r = benchmark(tms.xy_bounds, *tile)
    assert isinstance(r, BoundingBox)
