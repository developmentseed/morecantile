"""Pydantic modules for OGC TileMatrixSets (https://www.ogc.org/standards/tms)"""
import math
import os
from collections import namedtuple
from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel, Field
from rasterio.crs import CRS
from rasterio.warp import transform, transform_bounds

data_dir = os.path.join(os.path.dirname(__file__), "data")

NumType = Union[float, int]
BoundsType = Tuple[NumType, NumType]
WGS84_CRS = CRS.from_epsg(4326)

Tile = namedtuple("Tile", ["x", "y", "z"])
Coords = namedtuple("Coords", ["x", "y"])
CoordsBbox = namedtuple("CoordsBbox", ["xmin", "ymin", "xmax", "ymax"])


class NotAValidName(Exception):
    """Invalid TileMatrixSet name."""


class TileArgParsingError(Exception):
    """Raised when errors occur in parsing a function's tile arg(s)"""


def _parse_tile_arg(*args) -> Tile:
    """
    parse the *tile arg of module functions

    Parameters
    ----------
    tile : Tile or sequence of int
        May be be either an instance of Tile or 3 ints, X, Y, Z.

    Returns
    -------
    Tile

    Raises
    ------
    TileArgParsingError

    """
    if len(args) == 1:
        args = args[0]
    if len(args) == 3:
        return Tile(*args)
    else:
        raise TileArgParsingError(
            "the tile argument may have 1 or 3 values. Note that zoom is a keyword-only argument"
        )


def meters_per_unit(crs: CRS) -> float:
    """
    coefficient to convert the coordinate reference system (CRS)
    units into meters (metersPerUnit).

    From note g in http://docs.opengeospatial.org/is/17-083r2/17-083r2.html#table_2:
        If the CRS uses meters as units of measure for the horizontal dimensions,
        then metersPerUnit=1; if it has degrees, then metersPerUnit=2pa/360
        (a is the Earth maximum radius of the ellipsoid).

    """
    # crs.linear_units_factor[1]  GDAL 3.0
    return 1.0 if crs.linear_units == "metre" else 2 * math.pi * 6378137 / 360.0


class BoundingBox(BaseModel):
    """Bounding box"""

    type: str = Field("BoundingBoxType", const=True)
    crs: str = Field(..., regex=r"^http")
    lowerCorner: BoundsType
    upperCorner: BoundsType


class TileMatrix(BaseModel):
    """Tile matrix"""

    type: str = Field("TileMatrixType", const=True)
    title: Optional[str]
    abstract: Optional[str]
    keywords: Optional[List[str]]
    identifier: str
    scaleDenominator: float
    topLeftCorner: BoundsType
    tileWidth: int
    tileHeight: int
    matrixWidth: int
    matrixHeight: int

    class Config:
        """Forbid additional items like variableMatrixWidth."""

        extra = "forbid"


class TileMatrixSet(BaseModel):
    """Tile matrix set"""

    type: str = Field("TileMatrixSetType", const=True)
    title: str
    abstract: Optional[str]
    keywords: Optional[List[str]]
    identifier: str
    supportedCRS: str = Field(..., regex=r"^http://www.opengis.net/")
    wellKnownScaleSet: Optional[str] = Field(None, regex=r"^http")
    boundingBox: Optional[BoundingBox]
    tileMatrix: List[TileMatrix]

    @property
    def crs(self) -> CRS:
        """Fetch CRS from epsg"""
        return CRS.from_user_input(self.supportedCRS)

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
        tile_width: int = 256,
        tile_height: int = 256,
        matrix_scale: List = [1, 1],
        extent_crs: Optional[CRS] = None,
        minzoom: int = 0,
        maxzoom: int = 24,
        title: str = "Custom TileMatrixSet",
        identifier: str = "Custom",
    ):
        """
        Construct a custom TileMatrixSet.

        Attributes
        ----------
        crs: rasterio.crs.CRS
            Tile Matrix Set coordinate reference system
        extent: list
            Bounding box of the Tile Matrix Set, (left, bottom, right, top).
        tile_width: int
            Width of each tile of this tile matrix in pixels (default is 256).
        tile_height: int
            Height of each tile of this tile matrix in pixels (default is 256).
        matrix_scale: list
            Tiling schema coalescence coefficient (default: [1, 1] for EPSG:3857).
            Should be set to [2, 1] for EPSG:4326.
            see: http://docs.opengeospatial.org/is/17-083r2/17-083r2.html#14
        extent_crs: rasterio.crs.CRS
            Extent's coordinate reference system, as a rasterio CRS object.
            (default: same as input crs)
        minzoom: int
            Tile Matrix Set minimum zoom level (default is 0).
        maxzoom: int
            Tile Matrix Set maximum zoom level (default is 24).
        title: str
            Tile Matrix Set title (default is 'Custom TileMatrixSet')
        identifier: str
            Tile Matrix Set identifier (default is 'Custom')

        Returns:
        --------
        TileMatrixSet

        """
        epsg_number = crs.to_epsg()
        tms: Dict[str, Any] = {
            "title": title,
            "identifier": identifier,
            "supportedCRS": f"http://www.opengis.net/def/crs/EPSG/0/{epsg_number}",
            "tileMatrix": [],
        }

        bbox_epsg = extent_crs.to_epsg() if extent_crs else epsg_number
        tms["boundingBox"] = BoundingBox(
            **dict(
                crs=f"http://www.opengis.net/def/crs/EPSG/0/{bbox_epsg}",
                lowerCorner=[extent[0], extent[1]],
                upperCorner=[extent[2], extent[3]],
            )
        )

        bbox = CoordsBbox(
            *(
                transform_bounds(extent_crs, crs, *extent, densify_pts=21)
                if extent_crs
                else extent
            )
        )
        width = abs(bbox.xmax - bbox.xmin)
        height = abs(bbox.ymax - bbox.ymin)
        mpu = meters_per_unit(crs)
        for zoom in range(minzoom, maxzoom + 1):
            res = max(
                width / (tile_width * matrix_scale[0]) / 2.0 ** zoom,
                height / (tile_height * matrix_scale[1]) / 2.0 ** zoom,
            )
            tms["tileMatrix"].append(
                TileMatrix(
                    **dict(
                        identifier=str(zoom),
                        scaleDenominator=res * mpu / 0.00028,
                        topLeftCorner=[bbox.xmin, bbox.ymax],
                        tileWidth=tile_width,
                        tileHeight=tile_height,
                        matrixWidth=matrix_scale[0] * 2 ** zoom,
                        matrixHeight=matrix_scale[1] * 2 ** zoom,
                    )
                )
            )

        return cls(**tms)

    def matrix(self, zoom: int) -> TileMatrix:
        """Return the TileMatrix for a specific zoom."""
        try:
            return list(filter(lambda m: m.identifier == str(zoom), self.tileMatrix))[0]
        except IndexError:
            raise Exception(f"TileMatrix not found for level: {zoom}")

    def _resolution(self, matrix: TileMatrix) -> float:
        """
        Tile resolution for a TileMatrix.

        From note g in http://docs.opengeospatial.org/is/17-083r2/17-083r2.html#table_2:
          The pixel size of the tile can be obtained from the scaleDenominator
          by multiplying the later by 0.28 10-3 / metersPerUnit.

        """
        return matrix.scaleDenominator * 0.28e-3 / meters_per_unit(self.crs)

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
        matrix = self.matrix(zoom)

        res = self._resolution(matrix)
        xtile = int(
            math.floor(
                (xcoord - matrix.topLeftCorner[0])
                / float(res * matrix.tileWidth * (matrix.matrixWidth / (2 ** zoom)))
            )
        )
        ytile = int(
            math.floor(
                (matrix.topLeftCorner[1] - ycoord)
                / float(res * matrix.tileHeight * (matrix.matrixHeight / (2 ** zoom)))
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
        tile = _parse_tile_arg(*tile)
        matrix = self.matrix(tile.z)
        res = self._resolution(matrix)
        xcoord = matrix.topLeftCorner[0] + tile.x * res * matrix.tileWidth
        ycoord = matrix.topLeftCorner[1] - tile.y * res * matrix.tileHeight
        return Coords(xcoord, ycoord)

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
        tile = _parse_tile_arg(*tile)
        left, top = self._ul(*tile)
        right, bottom = self._ul(tile.x + 1, tile.y + 1, tile.z)
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
        tile = _parse_tile_arg(*tile)
        left, top = self.ul(tile.x, tile.y, tile.z)
        right, bottom = self.ul(tile.x + 1, tile.y + 1, tile.z)
        return CoordsBbox(left, bottom, right, top)

    def feature(
        self,
        tile: Tile,
        fid: Optional[str] = None,
        props: Optional[Dict] = None,
        precision: Optional[int] = None,
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
        feat: Dict[str, Any] = {
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
