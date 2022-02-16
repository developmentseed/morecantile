"""
morecantile is an adpatation of mapbox/mercantile to work with custom projection.

Refs:
    - mapproxy: https://github.com/mapproxy/mapproxy
    - mercantile: https://github.com/mapbox/mercantile
    - tiletanic: https://github.com/DigitalGlobe/tiletanic

"""

__version__ = "3.0.4"

from .commons import BoundingBox, Coords, Tile  # noqa
from .defaults import tms  # noqa
from .models import TileMatrixSet  # noqa
