"""Morecantile commons."""

from collections import OrderedDict, namedtuple

from rasterio.coords import BoundingBox  # noqa

_Tile = namedtuple("_Tile", ["x", "y", "z"])
_Coords = namedtuple("_Coords", ["x", "y"])


class Coords(_Coords):
    """A x,y Coordinates pair.

    Args:
        x (number): horizontal coordinate input projection unit.
        y (number): vertical coordinate input projection unit.

    Examples:
        >>> Coords(-90.3, 10.5)

    """

    def _asdict(self):
        return OrderedDict(zip(self._fields, self))


class Tile(_Tile):
    """TileMatrixSet X,Y,Z tile indices.

    Args:
        x (int): horizontal index.
        y (int): verctical index.
        z (int): zoom level.

    Examples:
        >>> Tile(0, 0, 0)

    """

    def _asdict(self):
        return OrderedDict(zip(self._fields, self))
