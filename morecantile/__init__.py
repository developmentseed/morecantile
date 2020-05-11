"""
morecantile is an adpatation of mapbox/mercantile to work with custom projection.

Refs:
    - mapproxy: https://github.com/mapproxy/mapproxy
    - mercantile: https://github.com/mapbox/mercantile
    - tiletanic: https://github.com/DigitalGlobe/tiletanic

"""

import os

import pkg_resources

from .models import Tile, TileMatrixSet  # noqa

version = pkg_resources.get_distribution(__package__).version

data_dir = os.path.join(os.path.dirname(__file__), "data")
default_grids = [
    os.path.splitext(f)[0] for f in os.listdir(data_dir) if f.endswith(".json")
]
