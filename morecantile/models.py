"""Pydantic modules for OGC TileMatrixSets (https://www.ogc.org/standards/tms)"""
import math
import os
import warnings
from typing import Any, Dict, Iterator, List, Optional, Sequence, Tuple, Union

from pydantic import AnyHttpUrl, BaseModel, Field, validator
from rasterio.crs import CRS, epsg_treats_as_latlong, epsg_treats_as_northingeasting
from rasterio.features import bounds as feature_bounds
from rasterio.warp import transform, transform_bounds, transform_geom

from .commons import BoundingBox, Coords, Tile
from .errors import InvalidIdentifier, PointOutsideTMSBounds
from .utils import (
    _parse_tile_arg,
    bbox_to_feature,
    meters_per_unit,
    point_in_bbox,
    truncate_lnglat,
)

NumType = Union[float, int]
BoundsType = Tuple[NumType, NumType]
LL_EPSILON = 1e-11
WGS84_CRS = CRS.from_epsg(4326)


class CRSType(CRS, AnyHttpUrl):
    """
    A geographic or projected coordinate reference system.
    """

    @classmethod
    def __get_validators__(cls):
        """validator for the type."""
        yield cls.validate

    @classmethod
    def validate(cls, value: Union[CRS, AnyHttpUrl]):
        """Validate CRS."""
        # If input is a string we tranlate it to CRS
        if not isinstance(value, CRS):
            return CRS.from_user_input(value)
        return value

    @classmethod
    def __modify_schema__(cls, field_schema):
        """Update default schema."""
        field_schema.update(
            anyOf=[
                {"type": "rasterio.crs.CRS"},
                {"type": "string", "minLength": 1, "maxLength": 65536, "format": "uri"},
            ],
            examples=[
                "CRS.from_epsg(4326)",
                "http://www.opengis.net/def/crs/EPSG/0/3978",
            ],
        )

    def __repr__(self):
        """Type representation."""
        return f"CRS({super().__repr__()})"


def CRS_to_uri(crs: CRS) -> str:
    """Convert CRS to URI."""
    epsg_code = crs.to_epsg()
    return f"http://www.opengis.net/def/crs/EPSG/0/{epsg_code}"


def crs_axis_inverted(crs: CRS) -> bool:
    """Check if CRS has inverted AXIS (lat,lon) instead of (lon,lat)."""
    return epsg_treats_as_latlong(crs) or epsg_treats_as_northingeasting(crs)


class TMSBoundingBox(BaseModel):
    """Bounding box"""

    type: str = Field("BoundingBoxType", const=True)
    crs: CRSType
    lowerCorner: BoundsType
    upperCorner: BoundsType

    class Config:
        """Configure TMSBoundingBox."""

        arbitrary_types_allowed = True
        json_encoders = {CRS: lambda v: CRS_to_uri(v)}


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
    supportedCRS: CRSType
    wellKnownScaleSet: Optional[AnyHttpUrl] = None
    boundingBox: Optional[TMSBoundingBox]
    tileMatrix: List[TileMatrix]

    class Config:
        """Configure TileMatrixSet."""

        arbitrary_types_allowed = True
        json_encoders = {CRS: lambda v: CRS_to_uri(v)}

    @validator("tileMatrix")
    def sort_tile_matrices(cls, v):
        """Sort matrices by identifier"""
        return sorted(v, key=lambda m: int(m.identifier))

    def __iter__(self):
        """Iterate over matrices"""
        for matrix in self.tileMatrix:
            yield matrix

    def __repr__(self):
        """Simplify default pydantic model repr."""
        return f"<TileMatrixSet title='{self.title}' identifier='{self.identifier}'>"

    @property
    def crs(self) -> CRS:
        """Fetch CRS from epsg"""
        return self.supportedCRS

    @property
    def minzoom(self) -> int:
        """TileMatrixSet minimum TileMatrix identifier"""
        return int(self.tileMatrix[0].identifier)

    @property
    def maxzoom(self) -> int:
        """TileMatrixSet maximum TileMatrix identifier"""
        return int(self.tileMatrix[-1].identifier)

    @property
    def _invert_axis(self) -> bool:
        """Check if CRS has inverted AXIS (lat,lon) instead of (lon,lat)."""
        return crs_axis_inverted(self.crs)

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
        tms: Dict[str, Any] = {
            "title": title,
            "identifier": identifier,
            "supportedCRS": crs,
            "tileMatrix": [],
        }

        is_inverted = False
        if crs.to_epsg():
            # We use URI because with EPSG code it doesn't work in GDAL 2
            crs_uri = CRS_to_uri(crs)
            is_inverted = crs_axis_inverted(CRS.from_user_input(crs_uri))

        if is_inverted:
            tms["boundingBox"] = TMSBoundingBox(
                crs=extent_crs or crs,
                lowerCorner=[extent[1], extent[0]],
                upperCorner=[extent[2], extent[3]],
            )
        else:
            tms["boundingBox"] = TMSBoundingBox(
                crs=extent_crs or crs,
                lowerCorner=[extent[0], extent[1]],
                upperCorner=[extent[2], extent[3]],
            )

        if extent_crs:
            bbox = BoundingBox(
                *transform_bounds(extent_crs, crs, *extent, densify_pts=21)
            )
        else:
            bbox = BoundingBox(*extent)

        x_origin = bbox.left if not is_inverted else bbox.top
        y_origin = bbox.top if not is_inverted else bbox.left

        width = abs(bbox.right - bbox.left)
        height = abs(bbox.top - bbox.bottom)
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
                        topLeftCorner=[x_origin, y_origin],
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
            tile_matrix = list(
                filter(lambda m: m.identifier == str(zoom), self.tileMatrix)
            )[0]
        except IndexError:
            matrix_scale = list(
                {
                    round(
                        self.tileMatrix[idx].scaleDenominator
                        / self.tileMatrix[idx - 1].scaleDenominator,
                        2,
                    )
                    for idx in range(1, len(self.tileMatrix))
                }
            )
            if len(matrix_scale) > 1:
                raise Exception(
                    f"TileMatrix not found for level: {zoom} - Unable to construct tileMatrix for TMS with variable scale"
                )

            warnings.warn(
                f"TileMatrix not found for level: {zoom} - Creating values from TMS Scale.",
                UserWarning,
            )

            tile_matrix = self.tileMatrix[-1]
            factor = 1 / matrix_scale[0]
            while not str(zoom) == tile_matrix.identifier:
                tile_matrix = TileMatrix(
                    **dict(
                        identifier=str(int(tile_matrix.identifier) + 1),
                        scaleDenominator=tile_matrix.scaleDenominator / factor,
                        topLeftCorner=tile_matrix.topLeftCorner,
                        tileWidth=tile_matrix.tileWidth,
                        tileHeight=tile_matrix.tileHeight,
                        matrixWidth=int(tile_matrix.matrixWidth * factor),
                        matrixHeight=int(tile_matrix.matrixHeight * factor),
                    )
                )

        return tile_matrix

    def _resolution(self, matrix: TileMatrix) -> float:
        """
        Tile resolution for a TileMatrix.

        From note g in http://docs.opengeospatial.org/is/17-083r2/17-083r2.html#table_2:
          The pixel size of the tile can be obtained from the scaleDenominator
          by multiplying the later by 0.28 10-3 / metersPerUnit.

        """
        return matrix.scaleDenominator * 0.28e-3 / meters_per_unit(self.crs)

    def zoom_for_res(
        self,
        res: float,
        max_z: Optional[int] = None,
        zoom_level_strategy: str = "auto",
    ) -> int:
        """Get TMS zoom level corresponding to a specific resolution.

        Args:
            res (float): Resolution in TMS unit.
            max_z (int): Maximum zoom level (default is tms maxzoom).
            zoom_level_strategy (str): Strategy to determine zoom level (same as in GDAL 3.2).
                LOWER will select the zoom level immediately below the theoretical computed non-integral zoom level.
                On the contrary, UPPER will select the immediately above zoom level.
                Defaults to AUTO which selects the closest zoom level.
                ref: https://gdal.org/drivers/raster/cog.html#raster-cog

        Returns:
            int: TMS zoom for a given resolution.

        Examples:
            >>> zoom_for_res(430.021)

        """
        if not max_z:
            max_z = self.maxzoom

        # Freely adapted from https://github.com/OSGeo/gdal/blob/dc38aa64d779ecc45e3cd15b1817b83216cf96b8/gdal/frmts/gtiff/cogdriver.cpp#L272-L305
        for zoom_level in range(max_z + 1):
            matrix_res = self._resolution(self.matrix(zoom_level))
            if res > matrix_res or abs(res - matrix_res) / matrix_res <= 1e-8:
                break

        if zoom_level > 0 and abs(res - matrix_res) / matrix_res > 1e-8:
            if zoom_level_strategy.lower() == "lower":
                zoom_level -= 1
            elif zoom_level_strategy.lower() == "upper":
                pass
            elif zoom_level_strategy.lower() == "auto":
                if (self._resolution(self.matrix(zoom_level - 1)) / res) < (
                    res / matrix_res
                ):
                    zoom_level -= 1
            else:
                raise ValueError(
                    f"Invalid strategy: {zoom_level_strategy}. Should be one of lower|upper|auto"
                )

        return zoom_level

    def lnglat(self, x: float, y: float, truncate=False) -> Coords:
        """Transform point(x,y) to longitude and latitude."""
        inside = point_in_bbox(Coords(x, y), self.xy_bbox)
        if not inside:
            warnings.warn(
                f"Point ({x}, {y}) is outside TMS bounds {list(self.xy_bbox)}.",
                PointOutsideTMSBounds,
            )

        xs, ys = transform(self.crs, WGS84_CRS, [x], [y])
        lng, lat = xs[0], ys[0]

        if truncate:
            lng, lat = truncate_lnglat(lng, lat)

        return Coords(lng, lat)

    def xy(self, lng: float, lat: float, truncate=False) -> Coords:
        """Transform longitude and latitude coordinates to TMS CRS."""
        if truncate:
            lng, lat = truncate_lnglat(lng, lat)

        inside = point_in_bbox(Coords(lng, lat), self.bbox)
        if not inside:
            warnings.warn(
                f"Point ({lng}, {lat}) is outside TMS bounds {list(self.bbox)}.",
                PointOutsideTMSBounds,
            )

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

        origin_x = (
            matrix.topLeftCorner[1] if self._invert_axis else matrix.topLeftCorner[0]
        )
        origin_y = (
            matrix.topLeftCorner[0] if self._invert_axis else matrix.topLeftCorner[1]
        )

        xtile = (
            math.floor((xcoord - origin_x) / float(res * matrix.tileWidth))
            if not math.isinf(xcoord)
            else 0
        )
        ytile = (
            math.floor((origin_y - ycoord) / float(res * matrix.tileHeight))
            if not math.isinf(ycoord)
            else 0
        )

        # # avoid out-of-range tiles
        if xtile < 0:
            xtile = 0

        if ytile < 0:
            ytile = 0

        if xtile > matrix.matrixWidth:
            xtile = matrix.matrixWidth

        if ytile > matrix.matrixHeight:
            ytile = matrix.matrixHeight

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

        origin_x = (
            matrix.topLeftCorner[1] if self._invert_axis else matrix.topLeftCorner[0]
        )
        origin_y = (
            matrix.topLeftCorner[0] if self._invert_axis else matrix.topLeftCorner[1]
        )

        xcoord = origin_x + tile.x * res * matrix.tileWidth
        ycoord = origin_y - tile.y * res * matrix.tileHeight
        return Coords(xcoord, ycoord)

    def xy_bounds(self, *tile: Tile) -> BoundingBox:
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
        return BoundingBox(left, bottom, right, top)

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

    def bounds(self, *tile: Tile) -> BoundingBox:
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
        return BoundingBox(left, bottom, right, top)

    @property
    def xy_bbox(self):
        """Return TMS bounding box in TileMatrixSet's CRS."""
        if self.boundingBox:
            left = (
                self.boundingBox.lowerCorner[1]
                if self._invert_axis
                else self.boundingBox.lowerCorner[0]
            )
            bottom = (
                self.boundingBox.lowerCorner[0]
                if self._invert_axis
                else self.boundingBox.lowerCorner[1]
            )
            right = (
                self.boundingBox.upperCorner[1]
                if self._invert_axis
                else self.boundingBox.upperCorner[0]
            )
            top = (
                self.boundingBox.upperCorner[0]
                if self._invert_axis
                else self.boundingBox.upperCorner[1]
            )
            if self.boundingBox.crs != self.crs:
                left, bottom, right, top = transform_bounds(
                    self.boundingBox.crs,
                    self.crs,
                    left,
                    bottom,
                    right,
                    top,
                    densify_pts=21,
                )

        else:
            zoom = self.minzoom
            matrix = self.matrix(zoom)
            left, top = self._ul(0, 0, zoom)
            right, bottom = self._ul(matrix.matrixWidth, matrix.matrixHeight, zoom)

        return BoundingBox(left, bottom, right, top)

    @property
    def bbox(self):
        """Return TMS bounding box in WGS84."""
        left, bottom, right, top = transform_bounds(
            self.crs, WGS84_CRS, *self.xy_bbox, densify_pts=21
        )
        return BoundingBox(left, bottom, right, top)

    def intersect_tms(self, bbox: BoundingBox) -> bool:
        """Check if a bounds intersects with the TMS bounds."""
        tms_bounds = self.xy_bbox
        return (
            (bbox[0] < tms_bounds[2])
            and (bbox[2] > tms_bounds[0])
            and (bbox[3] > tms_bounds[1])
            and (bbox[1] < tms_bounds[3])
        )

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

        for w, s, e, n in bboxes:
            for z in zooms:
                ul_tile = self.tile(w + LL_EPSILON, n - LL_EPSILON, z)
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
