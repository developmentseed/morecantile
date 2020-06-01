"""Pydantic modules for OGC TileMatrixSets (https://www.ogc.org/standards/tms)"""
import math
import os
import warnings
from typing import Any, Dict, Iterator, List, Optional, Sequence, Tuple, Union

from pydantic import AnyHttpUrl, BaseModel, Field, validator
from rasterio.crs import CRS
from rasterio.features import bounds as feature_bounds
from rasterio.warp import transform, transform_bounds, transform_geom

from .commons import Coords, CoordsBbox, Tile
from .errors import DeprecationWarning, InvalidIdentifier
from .utils import _parse_tile_arg, bbox_to_feature, meters_per_unit, truncate_lnglat

NumType = Union[float, int]
BoundsType = Tuple[NumType, NumType]
LL_EPSILON = 1e-11
WGS84_CRS = CRS.from_epsg(4326)


class BoundingBox(BaseModel):
    """Bounding box"""

    type: str = Field("BoundingBoxType", const=True)
    crs: AnyHttpUrl
    lowerCorner: BoundsType
    upperCorner: BoundsType


class TileMatrix(BaseModel):
    """Tile matrix"""

    type: str = Field("TileMatrixType", const=True)
    title: Optional[str]
    abstract: Optional[str]
    keywords: Optional[List[str]]
    identifier: str = Field(..., regex=r"^[0-9]+$")
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
    identifier: str = Field(..., regex=r"^[\w\d_\-]+$")
    supportedCRS: str = Field(..., regex=r"^http://www.opengis.net/")
    wellKnownScaleSet: Optional[AnyHttpUrl] = None
    boundingBox: Optional[BoundingBox]
    tileMatrix: List[TileMatrix]

    @validator("tileMatrix")
    def sort_tile_matrices(cls, v):
        """Sort matrices by identifier"""
        return sorted(v, key=lambda m: int(m.identifier))

    def __iter__(self):
        """Iterate over matrices"""
        for matrix in self.tileMatrix:
            yield matrix

    @property
    def crs(self) -> CRS:
        """Fetch CRS from epsg"""
        return CRS.from_user_input(self.supportedCRS)

    @property
    def minzoom(self) -> int:
        """TileMatrixSet minimum TileMatrix identifier"""
        return int(self.tileMatrix[0].identifier)

    @property
    def maxzoom(self) -> int:
        """TileMatrixSet maximum TileMatrix identifier"""
        return int(self.tileMatrix[-1].identifier)

    @classmethod
    def load(cls, name: str):
        """Load default TileMatrixSet."""
        warnings.warn(
            "TileMatrixSet.load will be deprecated in version 2.0.0", DeprecationWarning
        )
        try:
            data_dir = os.path.join(os.path.dirname(__file__), "data")
            return cls.parse_file(os.path.join(data_dir, f"{name}.json"))
        except FileNotFoundError:
            raise InvalidIdentifier(f"'{name}' is not a valid default TileMatrixSet.")

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

    def point_towgs84(self, x: float, y: float, truncate=False) -> Coords:
        """
        Transform point(x,y) to lat lon coordinates.

        Equivalent of mercantile.xy.

        """
        warnings.warn(
            "'point_towgs84' has been rename 'lnglat' and will be deprecated in version 2.0.0",
            DeprecationWarning,
        )
        xs, ys = transform(self.crs, WGS84_CRS, [x], [y])
        lng, lat = xs[0], ys[0]

        if truncate:
            lng, lat = truncate_lnglat(lng, lat)

        return Coords(lng, lat)

    def point_fromwgs84(self, lng: float, lat: float, truncate=False) -> Coords:
        """
        Transform point(x,y) from lat lon coordinates.

        Equivalent of mercantile.xy.

        """
        warnings.warn(
            "'point_fromwgs84' has been rename 'xy' and will be deprecated in version 2.0.0",
            DeprecationWarning,
        )
        if truncate:
            lng, lat = truncate_lnglat(lng, lat)

        xs, ys = transform(WGS84_CRS, self.crs, [lng], [lat])
        x, y = xs[0], ys[0]

        # https://github.com/mapbox/mercantile/blob/master/mercantile/__init__.py#L232-L237
        if lat <= -90:
            y = float("-inf")
        elif lat >= 90:
            y = float("inf")

        return Coords(x, y)

    def lnglat(self, x: float, y: float, truncate=False) -> Coords:
        """Transform point(x,y) to longitude and latitude."""
        xs, ys = transform(self.crs, WGS84_CRS, [x], [y])
        lng, lat = xs[0], ys[0]

        if truncate:
            lng, lat = truncate_lnglat(lng, lat)

        return Coords(lng, lat)

    def xy(self, lng: float, lat: float, truncate=False) -> Coords:
        """Transform longitude and latitude coordinates to TMS CRS."""
        if truncate:
            lng, lat = truncate_lnglat(lng, lat)

        xs, ys = transform(WGS84_CRS, self.crs, [lng], [lat])
        x, y = xs[0], ys[0]

        # https://github.com/mapbox/mercantile/blob/master/mercantile/__init__.py#L232-L237
        if lat <= -90:
            y = float("-inf")
        elif lat >= 90:
            y = float("inf")

        return Coords(x, y)

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
        xtile = math.floor(
            (xcoord - matrix.topLeftCorner[0]) / float(res * matrix.tileWidth)
        )
        ytile = math.floor(
            (matrix.topLeftCorner[1] - ycoord) / float(res * matrix.tileHeight)
        )
        return Tile(x=xtile, y=ytile, z=zoom)

    def tile(self, lng: float, lat: float, zoom: int, truncate=False) -> Tile:
        """
        Get the tile containing a longitude and latitude.

        Parameters
        ----------
        lng, lat : float
            A longitude and latitude pair in decimal degrees.
        zoom : int
            The web mercator zoom level.
        truncate : bool
            Whether or not to truncate inputs to limits of WGS84 bounds.

        Returns
        -------
        Tile

        """
        x, y = self.xy(lng, lat, truncate=truncate)
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
        return Coords(*self.lnglat(x, y))

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

    def tiles(
        self,
        west: float,
        south: float,
        east: float,
        north: float,
        zooms: Sequence[int],
        truncate: bool = False,
    ) -> Iterator[Tile]:
        """
        Get the tiles overlapped by a geographic bounding box

        Original code from https://github.com/mapbox/mercantile/blob/master/mercantile/__init__.py#L424

        Parameters
        ----------
        west, south, east, north : sequence of float
            Bounding values in decimal degrees.
        zooms : int or sequence of int
            One or more zoom levels.
        truncate : bool, optional
            Whether or not to truncate inputs to web mercator limits.

        Yields
        ------
        Tile

        Notes
        -----
        A small epsilon is used on the south and east parameters so that this
        function yields exactly one tile when given the bounds of that same tile.

        """
        if isinstance(zooms, int):
            zooms = (zooms,)

        if truncate:
            west, south = truncate_lnglat(west, south)
            east, north = truncate_lnglat(east, north)

        if west > east:
            bbox_west = (-180.0, south, east, north)
            bbox_east = (west, south, 180.0, north)
            bboxes = [bbox_west, bbox_east]
        else:
            bboxes = [(west, south, east, north)]

        tms_bounds = self.bounds(Tile(0, 0, 0))
        for w, s, e, n in bboxes:
            w = max(tms_bounds[0], w)
            s = max(tms_bounds[1], s)
            e = min(tms_bounds[2], e)
            n = min(tms_bounds[3], n)
            for z in zooms:
                ul_tile = self.tile(w, n, z)
                lr_tile = self.tile(e - LL_EPSILON, s + LL_EPSILON, z)

                for i in range(ul_tile.x, lr_tile.x + 1):
                    for j in range(ul_tile.y, lr_tile.y + 1):
                        yield Tile(i, j, z)

    def feature(
        self,
        tile: Tile,
        fid: Optional[str] = None,
        props: Dict = {},
        buffer: Optional[NumType] = None,
        precision: Optional[int] = None,
        projected: bool = False,
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
        buffer : float, optional
            Optional buffer distance for the GeoJSON polygon.
        precision: float
            If >= 0, geometry coordinates will be rounded to this number of decimal,
            otherwise original coordinate values will be preserved (default).
        projected : bool, optional
            Return coordinates in TMS projection. Default is false.

        Returns
        -------
        dict

        """
        west, south, east, north = self.xy_bounds(tile)

        if not projected:
            geom = bbox_to_feature(west, south, east, north)
            geom = transform_geom(self.crs, WGS84_CRS, geom)
            west, south, east, north = feature_bounds(geom)

        if buffer:
            west -= buffer
            south -= buffer
            east += buffer
            north += buffer

        if precision and precision >= 0:
            west, south, east, north = (
                round(v, precision) for v in (west, south, east, north)
            )

        bbox = [min(west, east), min(south, north), max(west, east), max(south, north)]
        geom = bbox_to_feature(west, south, east, north)

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

        if projected:
            warnings.warn(
                "CRS is no longer part of the GeoJSON specification."
                "Other projection than EPSG:4326 might not be supported.",
                UserWarning,
            )
            feat.update(
                {"crs": {"type": "EPSG", "properties": {"code": self.crs.to_epsg()}}}
            )

        if props:
            feat["properties"].update(props)

        if fid is not None:
            feat["id"] = fid

        return feat
