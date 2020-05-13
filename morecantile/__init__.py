"""
morecantile is an adpatation of mapbox/mercantile to work with custom projection.

Refs:
    - mapproxy: https://github.com/mapproxy/mapproxy
    - mercantile: https://github.com/mapbox/mercantile
    - tiletanic: https://github.com/DigitalGlobe/tiletanic

"""

import pkg_resources

from .commons import Coords, CoordsBbox, Tile  # noqa
from .defaults import tms  # noqa
from .models import TileMatrixSet  # noqa

version = pkg_resources.get_distribution(__package__).version
