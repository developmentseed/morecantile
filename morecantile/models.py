"""Pydantic modules for OGC TileMatrixSets (https://www.ogc.org/standards/tms)"""
from typing import Dict, List, Optional, Tuple, Union

import os
import math
from pydantic import BaseModel, Field
from collections import namedtuple

import mercantile
from rasterio.crs import CRS
from rasterio.warp import transform

data_dir = os.path.join(os.path.dirname(__file__), "data")

NumType = Union[float, int]
BoundsType = Tuple[NumType, NumType]
WGS84_CRS = CRS.from_epsg(4326)

Tile = namedtuple("Tile", ["x", "y", "z"])
Coords = namedtuple("Coords", ["x", "y"])
CoordsBbox = namedtuple("CoordsBbox", ["xmin", "ymin", "xmax", "ymax"])


class NotAValidName(Exception):
    """Invalid TileMatrixSet name."""


class BoundingBox(BaseModel):
    """Bounding box"""

    type: str = Field("BoundingBoxType", const=True)
    crs: str = Field(..., regex=r"^http")
    lowerCorner: BoundsType
    upperCorner: BoundsType


class TileMatrix(BaseModel):
    """Tile matrix"""

    type: str = Field("TileMatrixType", const=True)
    identifier: str
    scaleDenominator: float
    topLeftCorner: BoundsType
    tileWidth: int
    tileHeight: int
    matrixWidth: int
    matrixHeight: int


class TileMatrixSet(BaseModel):
    """Tile matrix set"""

    type: str = Field("TileMatrixSetType", const=True)
    title: str
    identifier: str
    supportedCRS: str = Field(..., regex=r"^http://www.opengis.net/def/crs/EPSG")
    wellKnownScaleSet: Optional[str] = Field(None, regex=r"^http")
    boundingBox: Optional[BoundingBox]
    tileMatrix: List[TileMatrix]

    @property
    def crs(self) -> CRS:
        """Fetch CRS from epsg"""
        return CRS.from_epsg(self.supportedCRS.split("/")[-1])

    @property
    def meters_per_unit(self) -> float:
        """coefficient to convert the coordinate reference system (CRS)
        units into meters (metersPerUnit)
        """
        # self.crs.linear_units_factor[1]  GDAL 3.0
        return (
            1.0 if self.crs.linear_units == "metre" else 2 * math.pi * 6378137 / 360.0
        )

    @classmethod
    def load(cls, name: str):
        """Load default TileMatrixSet."""
        try:
            return cls.parse_file(os.path.join(data_dir, f"{name}.json"))
        except FileNotFoundError:
            raise NotAValidName(f"'{name}' is not a valid default TileMatrixSet.")

    @classmethod
    def custom(
        cls,
        extent: List[float],
        crs: CRS,
        resolution: float,
        tile_width: int = 256,
        tile_height: int = 256,
        matrix_scale: List = [1, 1],
    ):
        """
        Construct a custom TileMatrixSet.

        Attributes
        ----------
        crs: rasterio.crs.CRS
            TileMatrixSet coordinate reference system
        extent: list
            Bounding box of the TileMatrixSet
        resolution: float
        matrix_scale: list
            Tiling schema coalescence coefficient (default: [1, 1] for EPSG:3857).
            Should be set to [2, 1] for EPSG:4326.
            see: http://docs.opengeospatial.org/is/17-083r2/17-083r2.html#14

        Returns:
        --------
        TileMatrixSet
        """
        raise NotImplementedError

    def matrix(self, zoom: int) -> TileMatrix:
        """Return the TileMatrix for a specific zoom."""
        zoom_str = str(zoom)
        for matrix in self.tileMatrix:
            if matrix.identifier == zoom_str:
                return matrix

        raise Exception(f"TileMatrix not found for level: {zoom}")

    def _resolution(self, matrix: TileMatrix) -> float:
        """Tile resolution for a zoom level."""
        # TODO
        # width = abs(self.extent.xmax - self.extent.xmin)
        # height = abs(self.extent.ymax - self.extent.ymin)
        # return max(
        #     width / (self.tile_size[0] * self.matrix_scale[0]) / 2.0 ** zoom,
        #     height / (self.tile_size[1] * self.matrix_scale[1]) / 2.0 ** zoom,
        # )

    def point_towgs84(self, x: float, y: float) -> Tuple[float, float]:
        """Transform point(x,y) to lat lon coordinates."""
        xs, ys = transform(self.crs, WGS84_CRS, [x], [y])
        return xs[0], ys[0]

    def point_fromwgs84(self, x: float, y: float) -> Tuple[float, float]:
        """Transform point(x,y) from lat lon coordinates."""
        xs, ys = transform(WGS84_CRS, self.crs, [x], [y])
        return xs[0], ys[0]

    def _tile(self, xcoord: float, ycoord: float, zoom: int) -> Tile:
        """
        Get the tile containing a Point (in input projection).

        Parameters
        ----------
        xcoord, ycoord : float
            A longitude and latitude pair in input projection.
        zoom : int
            The zoom level.

        Returns
        -------
        Tile

        """
        # TODO
        # matrix = self.matrix(zoom)
        # res = self._resolution(zoom)
        # xtile = int(
        #     math.floor(
        #         (xcoord - self.extent.xmin)
        #         / float(res * self.tile_size[0] * self.matrix_scale[0])
        #     )
        # )
        # ytile = int(
        #     math.floor(
        #         (self.extent.ymax - ycoord)
        #         / float(res * self.tile_size[1] * self.matrix_scale[1])
        #     )
        # )
        # return Tile(x=xtile, y=ytile, z=zoom)

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
        # TODO
        # tile = mercantile._parse_tile_arg(*tile)
        # xtile, ytile, zoom = tile
        # matrix = self.matrix(zoom)
        # res = self._resolution(zoom)
        # xcoord = self.extent.xmin + xtile * res * self.tile_size[0]
        # ycoord = self.extent.ymax - ytile * res * self.tile_size[1]
        # return xcoord, ycoord

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
                "grid_name": self.identifier,
                "grid_crs": self.crs.to_string(),
            },
        }
        if props:
            feat["properties"].update(props)

        if fid is not None:
            feat["id"] = fid

        return feat
