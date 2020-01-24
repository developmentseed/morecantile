"""
morecantile is an adpatation of mapbox/mercantile to work with custom projection.

Refs:
    - mapproxy: https://github.com/mapproxy/mapproxy
    - mercantile: https://github.com/mapbox/mercantile
    - tiletanic: https://github.com/DigitalGlobe/tiletanic

"""

from typing import Dict, List, Tuple

import re
import math
import pkg_resources
from collections import namedtuple

from rasterio.crs import CRS
from rasterio.warp import transform_bounds, transform

import mercantile

version = pkg_resources.get_distribution(__package__).version

qk_regex = re.compile(r"[0-3]+$")

Tile = mercantile.Tile
"""
From https://github.com/mapbox/mercantile
"""

Coords = namedtuple("Coords", ["x", "y"])
"""
A X,Y Coordinates pair.

Attributes
----------
    X, Y : float
        X, Y coordinates in input projection unit.
"""

CoordsBbox = namedtuple("CoordsBbox", ["xmin", "ymin", "xmax", "ymax"])
"""
A geographic bounding box.

Attributes
----------
    xmin, ymin, xmax, ymax : float
        Bounding values in input projection unit.
"""

quadkey = mercantile.quadkey
quadkey_to_tile = mercantile.quadkey_to_tile
parent = mercantile.parent
children = mercantile.children
"""
Utility functions from https://github.com/mapbox/mercantile
"""


class _grids(object):
    """Default Grids info."""

    _default_grids = {
        4326: {"extent": [-180, -90, 180, 90], "matrix_scale": [2, 1]},
        # Elliptical Mercator projection
        3395: {
            "extent": [-20037508.34279, -15496570.73972, 20037508.34279, 18764656.23138]
        },
        # Spherical Mercator
        3857: {
            "extent": [
                -20037508.342789244,
                -20037508.342789244,
                20037508.342789244,
                20037508.342789244,
            ]
        },
        # WGS 84 / NSIDC Sea Ice Polar Stereographic North
        3413: {"extent": [-2353926.81, 2345724.36, -382558.89, 383896.60]},
        # WGS 84 / Antarctic Polar Stereographic
        3031: {"extent": [-948.75, -543592.47, 5817.41, -3333128.95]},
        # ETRS89-extended / LAEA Europe
        3035: {"extent": [1896628.62, 1507846.05, 4662111.45, 6829874.45]},
    }

    def get(self, key: int) -> Tuple[CRS, Dict]:
        """Return default grid meta."""
        try:
            return CRS.from_epsg(key), self._default_grids[key]
        except KeyError:
            raise Exception(f"{key} is not a defaults grids")


default_grids = _grids()


class TileSchema(object):
    """
    Custom Tiling schema.

    Ref: OGC Tile Matrix Specification http://docs.opengeospatial.org/is/17-083r2/17-083r2.html
    """

    def __init__(
        self,
        crs: CRS = CRS({"init": "EPSG:3857"}),
        extent: List[float] = [
            -20037508.342789244,
            -20037508.342789244,
            20037508.342789244,
            20037508.342789244,
        ],
        extent_crs: CRS = None,
        tile_size: List[int] = [256, 256],
        matrix_scale: List[int] = [1, 1],
    ) -> None:
        """
        Construct a custom tile scheme.

        Attributes
        ----------
            crs: rasterio.crs.CRS
                Tiling schema coordinate reference system, as a rasterio CRS object
                (default: CRS({'init': 'EPSG:3857'}))
            extent: list
                Bounding box of the tiling schema (default: [-20037508.342789244, -20037508.342789244, 20037508.342789244, 20037508.342789244])
            extent_crs: rasterio.crs.CRS
                Extent's coordinate reference system, as a rasterio CRS object.
                (default: assuming same as input crs)
            tile_size: list
                Tiling schema tile sizes (default: [256, 256])
            matrix_scale: list
                Tiling schema coalescence coefficient (default: [1, 1] for EPSG:3857).
                Should be set to [2, 1] for EPSG:4326.
                see: http://docs.opengeospatial.org/is/17-083r2/17-083r2.html#14

        """
        self.crs = crs
        bbox = (
            transform_bounds(extent_crs, self.crs, *extent, densify_pts=21)
            if extent_crs
            else extent
        )
        self.extent = CoordsBbox(*bbox)
        self.wgs84extent = transform_bounds(
            self.crs, CRS({"init": "EPSG:4326"}), *self.extent, densify_pts=21
        )
        self.origin = Coords(float(self.extent.xmin), float(self.extent.ymax))
        self.tile_size = tile_size
        self.matrix_scale = matrix_scale
        self.meters_per_unit = (
            # self.crs.linear_units_factor[1]  GDAL 3.0
            1.0
            if self.crs.linear_units == "metre"
            else 2 * math.pi * 6378137 / 360.0
        )

    def point_towgs84(self, x: float, y: float) -> Tuple[float, float]:
        """Transform point(x,y) to lat lon coordinates."""
        xs, ys = transform(self.crs, CRS({"init": "EPSG:4326"}), [x], [y])
        return xs[0], ys[0]

    def point_fromwgs84(self, x: float, y: float) -> Tuple[float, float]:
        """Transform point(x,y) from lat lon coordinates."""
        xs, ys = transform(CRS({"init": "EPSG:4326"}), self.crs, [x], [y])
        return xs[0], ys[0]

    def _resolution(self, zoom: int) -> float:
        """Tile resolution for a zoom level."""
        width = abs(self.extent.xmax - self.extent.xmin)
        height = abs(self.extent.ymax - self.extent.ymin)
        return max(
            width / (self.tile_size[0] * self.matrix_scale[0]) / 2.0 ** zoom,
            height / (self.tile_size[1] * self.matrix_scale[1]) / 2.0 ** zoom,
        )

    def get_ogc_tilematrix(self, zoom: int) -> Dict:
        """
        Construct TileMatrixType dict.

        Attributes
        ----------
            zoom: the zoom level

        Returns
        -------
            Dict of the OGC TileMatrix information.

        """
        return {
            "type": "TileMatrixType",
            "identifier": str(zoom),
            "scaleDenominator": self._resolution(zoom) * self.meters_per_unit / 0.00028,
            "topLeftCorner": list(self.origin),
            "tileWidth": self.tile_size[0],
            "tileHeight": self.tile_size[1],
            "matrixWidth": self.matrix_scale[0] * 2 ** zoom,
            "matrixHeight": self.matrix_scale[1] * 2 ** zoom,
        }

    def _tile(self, xcoord: float, ycoord: float, zoom: int) -> Tile:
        """
        Get the tile containing a Point (in input projection).

        Parameters
        ----------
            xcoord, ycoord : float
                A longitude and latitude pair in input projection.
            zoom : int
                The web mercator zoom level.

        Returns
        -------
            Tile

        """
        res = self._resolution(zoom)
        xtile = int(
            math.floor(
                (xcoord - self.extent.xmin)
                / float(res * self.tile_size[0] * self.matrix_scale[0])
            )
        )
        ytile = int(
            math.floor(
                (self.extent.ymax - ycoord)
                / float(res * self.tile_size[1] * self.matrix_scale[1])
            )
        )
        return Tile(x=xtile, y=ytile, z=zoom)

    def tile(self, lng: float, lat: float, zoom: int) -> Tile:
        """
        Get the tile containing a longitude and latitude.

        Parameters
        ----------
            lng, lat : float
                A longitude and latitude pair in decimal degrees.
            zoom : int
                The web mercator zoom level.

        Returns
        -------
            Tile

        """
        x, y = self.point_fromwgs84(lng, lat)
        return self._tile(x, y, zoom)

    def _ul(self, *tile: Tile) -> Coords:
        """
        Return the upper left coordinate of the (x, y, z) tile in input projection.

        Attributes
        ----------
            tile: (x, y, z) tile coordinates or a Tile object we want the upper left geospatial coordinates of.

        Returns
        -------
            The upper left geospatial coordiantes of the input tile.

        """
        tile = mercantile._parse_tile_arg(*tile)
        xtile, ytile, zoom = tile

        res = self._resolution(zoom)
        xcoord = self.extent.xmin + xtile * res * self.tile_size[0]
        ycoord = self.extent.ymax - ytile * res * self.tile_size[1]
        return xcoord, ycoord

    def xy_bounds(self, *tile: Tile) -> CoordsBbox:
        """
        Return the bounding box of the (x, y, z) tile in input projection.

        Attributes
        ----------
            tile: A tuple of (x, y, z) tile coordinates or a Tile object we want the bounding box of.

        Returns
        -------
            The bounding box of the input tile.

        """
        tile = mercantile._parse_tile_arg(*tile)
        xtile, ytile, zoom = tile
        left, top = self._ul(xtile, ytile, zoom)
        right, bottom = self._ul(xtile + 1, ytile + 1, zoom)
        return CoordsBbox(left, bottom, right, top)

    def ul(self, *tile: Tile) -> Coords:
        """
        Return the upper left coordinate of the (x, y, z) tile in Lat Lon.

        Attributes
        ----------
            tile: (x, y, z) tile coordinates or a Tile object we want the upper left geospatial coordinates of.

        Returns
        -------
            The upper left geospatial coordiantes of the input tile.

        """
        x, y = self._ul(*tile)
        return Coords(*self.point_towgs84(x, y))

    def bounds(self, *tile: Tile) -> CoordsBbox:
        """
        Return the bounding box of the (x, y, z) tile in LatLong.

        Attributes
        ----------
            tile: A tuple of (x, y, z) tile coordinates or a Tile object we want the bounding box of.

        Returns
        -------
            The bounding box of the input tile.

        """
        tile = mercantile._parse_tile_arg(*tile)
        xtile, ytile, zoom = tile
        left, top = self.ul(xtile, ytile, zoom)
        right, bottom = self.ul(xtile + 1, ytile + 1, zoom)
        return CoordsBbox(left, bottom, right, top)

    def feature(
        self, tile: Tile, fid: str = None, props: Dict = None, precision: float = None
    ) -> Dict:
        """
        Get the GeoJSON feature corresponding to a tile.

        Originaly from https://github.com/mapbox/mercantile/blob/master/mercantile/__init__.py

        Parameters
        ----------
            tile : Tile or sequence of int
                May be be either an instance of Tile or 3 ints, X, Y, Z.
            fid : str, optional
                A feature id.
            props : dict, optional
                Optional extra feature properties.
            precision : int, optional
                GeoJSON coordinates will be truncated to this number of decimal
                places.
        Returns
        -------
            dict

        """
        west, south, east, north = self.bounds(tile)

        if precision and precision >= 0:
            west, south, east, north = (
                round(v, precision) for v in (west, south, east, north)
            )
        bbox = [min(west, east), min(south, north), max(west, east), max(south, north)]
        geom = {
            "type": "Polygon",
            "coordinates": [
                [
                    [west, south],
                    [west, north],
                    [east, north],
                    [east, south],
                    [west, south],
                ]
            ],
        }
        xyz = str(tile)
        feat = {
            "type": "Feature",
            "bbox": bbox,
            "id": xyz,
            "geometry": geom,
            "properties": {
                "title": f"XYZ tile {xyz}",
                "grid_crs": self.crs.to_string(),
            },
        }
        if props:
            feat["properties"].update(props)

        if fid is not None:
            feat["id"] = fid

        return feat
