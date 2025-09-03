"""
morecantile is an adaptation of mapbox/mercantile to work with custom projection.

Refs:
    - mapproxy: https://github.com/mapproxy/mapproxy
    - mercantile: https://github.com/mapbox/mercantile
    - tiletanic: https://github.com/DigitalGlobe/tiletanic

"""

__version__ = "6.2.0"

from .commons import BoundingBox, Coords, Tile  # noqa
from .defaults import TileMatrixSets, tms  # noqa
from .models import TileMatrixSet  # noqa
