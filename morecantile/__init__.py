"""
morecantile is an adaptation of mapbox/mercantile to work with custom projection.

Refs:
    - mapproxy: https://github.com/mapproxy/mapproxy
    - mercantile: https://github.com/mapbox/mercantile
    - tiletanic: https://github.com/DigitalGlobe/tiletanic

"""

__version__ = "7.0.3"

from .commons import BoundingBox, Coords, Tile
from .defaults import TileMatrixSets, tms
from .models import TileMatrixSet

__all__ = [
    "BoundingBox",
    "Coords",
    "Tile",
    "TileMatrixSet",
    "TileMatrixSets",
    "tms",
]
