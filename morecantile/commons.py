"""Morecantile commons."""

from collections import namedtuple

Tile = namedtuple("Tile", ["x", "y", "z"])
"""
An TMS tile

Attributes
----------
x, y, z : int
    x and y indexes of the tile and zoom level z.
"""

Coords = namedtuple("Coords", ["x", "y"])
"""
A x,y Coordinates pair.

Attributes
----------
x, y : float
    x, y coordinates in input projection unit.
"""

CoordsBbox = namedtuple("CoordsBbox", ["xmin", "ymin", "xmax", "ymax"])
"""
A geographic bounding box.

Attributes
----------
xmin, ymin, xmax, ymax : float
    Bounding values in input projection unit.

"""
