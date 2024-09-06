"""Morecantile commons."""

from typing import NamedTuple


class BoundingBox(NamedTuple):
    """A xmin,ymin,xmax,ymax coordinates tuple.

    Args:
        left (number): min horizontal coordinate.
        bottom (number):min vertical coordinate.
        right (number): max horizontal coordinate.
        top (number): max vertical coordinate.

    Examples:
        >>> BoundingBox(-180.0, -90.0, 180.0, 90.0)

    """

    left: float
    bottom: float
    right: float
    top: float


class Coords(NamedTuple):
    """A x,y Coordinates pair.

    Args:
        x (number): horizontal coordinate input projection unit.
        y (number): vertical coordinate input projection unit.

    Examples:
        >>> Coords(-90.3, 10.5)

    """

    x: float
    y: float


class Tile(NamedTuple):
    """TileMatrixSet X,Y,Z tile indices.

    Args:
        x (int): horizontal index.
        y (int): verctical index.
        z (int): zoom level.

    Examples:
        >>> Tile(0, 0, 0)

    """

    x: int
    y: int
    z: int
