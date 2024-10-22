"""Morecantile/Mercantile/Utiles comparison benchmark

The benchmark suite is adapted from jessekrubin/utiles
https://github.com/jessekrubin/utiles/blob/ea58b9a017a2e3528f03cc20f16ef531737b863f/utiles-pyo3/bench/test_bench.py#L17-L25
"""
# This file is a modified version of https://github.com/jessekrubin/utiles/blob/ea58b9a017a2e3528f03cc20f16ef531737b863f/utiles-pyo3/bench/test_bench.py.
#
# The original license follows.
#
# MIT License
#
# Copyright (c) 2023 jessekrubin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import Callable, Tuple

import mercantile
import pytest
import utiles

import morecantile

tms = morecantile.tms.get("WebMercatorQuad")

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


@pytest.mark.parametrize(
    "tile",
    [pytest.param(t, id=str(t)) for t in TEST_TILES],
)
@pytest.mark.parametrize(
    "func",
    [
        pytest.param(mercantile.bounds, id="mercantile"),
        pytest.param(tms.bounds, id="morecantile"),
        pytest.param(utiles.bounds, id="utiles"),
    ],
)
@pytest.mark.benchmark(group="bounds")
def test_bounds(
    tile: Tuple[int, int, int],
    func: Callable[[Tuple[int, int, int]], Tuple[float, float]],
    benchmark,
) -> None:
    """Benchmark bounds() method."""
    _ = benchmark(func, *tile)


@pytest.mark.parametrize(
    "tile",
    [pytest.param(t, id=str(t)) for t in TEST_TILES],
)
@pytest.mark.parametrize(
    "func",
    [
        pytest.param(mercantile.xy_bounds, id="mercantile"),
        pytest.param(tms.xy_bounds, id="morecantile"),
        pytest.param(utiles.xy_bounds, id="utiles"),
    ],
)
@pytest.mark.benchmark(group="xy_bounds")
def test_xy_bounds(
    tile: Tuple[int, int, int],
    func: Callable[[Tuple[int, int, int]], Tuple[float, float]],
    benchmark,
) -> None:
    """Benchmark xy_bounds() method."""
    _ = benchmark(func, *tile)
