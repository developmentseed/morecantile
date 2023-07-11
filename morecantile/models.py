"""Pydantic modules for OGC TileMatrixSets (https://www.ogc.org/standards/tms)"""

import math
import warnings
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Iterator,
    List,
    Literal,
    Optional,
    Sequence,
    Tuple,
    Union,
)

from cachetools import LRUCache, cached
from cachetools.keys import hashkey
from pydantic import (
    AnyHttpUrl,
    AnyUrl,
    BaseModel,
    Field,
    PrivateAttr,
    conlist,
    validator,
)
from pyproj import CRS, Transformer
from pyproj.exceptions import CRSError, ProjError

from morecantile.commons import BoundingBox, Coords, Tile
from morecantile.errors import (
    DeprecationError,
    InvalidZoomError,
    NoQuadkeySupport,
    PointOutsideTMSBounds,
    QuadKeyError,
)
from morecantile.utils import (
    _parse_tile_arg,
    bbox_to_feature,
    check_quadkey_support,
    meters_per_unit,
    point_in_bbox,
    to_rasterio_crs,
)

NumType = Union[float, int]
BoundsType = Tuple[NumType, NumType]
LL_EPSILON = 1e-11
WGS84_CRS = CRS.from_epsg(4326)


if TYPE_CHECKING:
    axesInfo = List[str]
else:
    axesInfo = conlist(str, min_items=2, max_items=2)


class CRSUri(BaseModel):
    """Coordinate Reference System (CRS) from URI."""

    uri: AnyUrl = Field(
        ...,
        description="Reference to one coordinate reference system (CRS) as URI",
        examples=[
            "http://www.opengis.net/def/crs/EPSG/0/3978",
            "urn:ogc:def:crs:EPSG::2193",
        ],
    )


class CRSWKT(BaseModel):
    """Coordinate Reference System (CRS) from WKT."""

    wkt: str = Field(
        ...,
        description="Reference to one coordinate reference system (CRS) as WKT string",
        examples=[
            'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]]',
        ],
    )


# NOT SUPPORTED
# class CRSRef(BaseModel):
#     """CRS from referenceSystem."""
#
#     referenceSystem: Dict[str, Any] = Field(
#         ...,
#         description="A reference system data structure as defined in the MD_ReferenceSystem of the ISO 19115",
#     )


class CRSType(BaseModel):
    """CRS model.

    Ref: https://github.com/opengeospatial/ogcapi-tiles/blob/master/openapi/schemas/common-geodata/crs.yaml

    Code generated using https://github.com/koxudaxi/datamodel-code-generator/
    """

    __root__: Union[str, Union[CRSUri, CRSWKT]] = Field(..., title="CRS")
    _pyproj_crs: CRS = PrivateAttr()

    def __init__(self, **data):
        """Custom Init to validate CRS string and create Pyproj CRS object."""
        super().__init__(**data)

        self._pyproj_crs = CRS.from_user_input(data.get("__root__"))

    @property
    def srs(self) -> str:
        """return the string form of the user input used to create the CRS."""
        return self._pyproj_crs.srs

    def to_epsg(self, *args: Any, **kwargs: Any) -> Optional[int]:
        """return EPSG number of the CRS."""
        return self._pyproj_crs.to_epsg(*args, **kwargs)

    def to_wkt(self, *args: Any, **kwargs: Any) -> str:
        """return WKT version of the CRS."""
        return self._pyproj_crs.to_wkt(*args, **kwargs)

    def to_proj4(self, *args: Any, **kwargs: Any) -> str:
        """return PROJ4 version of the CRS."""
        return self._pyproj_crs.to_proj4(*args, **kwargs)

    def to_dict(self) -> Dict:
        """return DICT version of the CRS."""
        return self._pyproj_crs.to_dict()

    def to_json(self, *args: Any, **kwargs: Any) -> str:
        """return JSON version of the CRS."""
        return self._pyproj_crs.to_json(*args, **kwargs)


def CRS_to_uri(crs: CRS) -> str:
    """Convert CRS to URI."""
    authority = "EPSG"
    code = None
    version = "0"
    # attempt to grab the authority, version, and code from the CRS
    authority_code = crs.to_authority(min_confidence=20)
    if authority_code is not None:
        authority, code = authority_code
        # if we have a version number in the authority, split it out
        if "_" in authority:
            authority, version = authority.split("_")
    return f"http://www.opengis.net/def/crs/{authority}/{version}/{code}"


def crs_axis_inverted(crs: CRS) -> bool:
    """Check if CRS has inverted AXIS (lat,lon) instead of (lon,lat)."""
    return crs.axis_info[0].abbrev.upper() in ["Y", "LAT", "N"]


def ordered_axis_inverted(ordered_axes: List[str]) -> bool:
    """Check if ordered axes have inverted AXIS (lat,lon) instead of (lon,lat)."""
    return ordered_axes[0].upper() in ["Y", "LAT", "N"]


class TMSBoundingBox(BaseModel):
    """Bounding box

    ref: https://github.com/opengeospatial/2D-Tile-Matrix-Set/blob/master/schemas/tms/2.0/json/2DBoundingBox.json

    """

    lowerLeft: BoundsType = Field(
        description="A 2D Point in the CRS indicated elsewhere"
    )
    upperRight: BoundsType = Field(
        description="A 2D Point in the CRS indicated elsewhere"
    )
    crs: Optional[CRSType]
    orderedAxes: Optional[axesInfo]

    class Config:
        """Configure TMSBoundingBox."""

        arbitrary_types_allowed = True


# class variableMatrixWidth(BaseModel):
#     """Variable Matrix Width Definition


#     ref: https://github.com/opengeospatial/2D-Tile-Matrix-Set/blob/master/schemas/tms/2.0/json/variableMatrixWidth.json
#     """

#     coalesce: int = Field(..., ge=2, multiple_of=1, description="Number of tiles in width that coalesce in a single tile for these rows")
#     minTileRow: int = Field(..., ge=0, multiple_of=1, description="First tile row where the coalescence factor applies for this tilematrix")
#     maxTileRow: int = Field(..., ge=0, multiple_of=1, description="Last tile row where the coalescence factor applies for this tilematrix")


class TileMatrix(BaseModel):
    """Tile Matrix Definition

    A tile matrix, usually corresponding to a particular zoom level of a TileMatrixSet.

    ref: https://github.com/opengeospatial/2D-Tile-Matrix-Set/blob/master/schemas/tms/2.0/json/tileMatrix.json
    """

    title: Optional[str] = Field(
        description="Title of this tile matrix, normally used for display to a human"
    )
    description: Optional[str] = Field(
        description="Brief narrative description of this tile matrix set, normally available for display to a human"
    )
    keywords: Optional[List[str]] = Field(
        description="Unordered list of one or more commonly used or formalized word(s) or phrase(s) used to describe this dataset"
    )
    id: str = Field(
        ...,
        regex=r"^[0-9]+$",
        description="Identifier selecting one of the scales defined in the TileMatrixSet and representing the scaleDenominator the tile. Implementation of 'identifier'",
    )
    scaleDenominator: float = Field(
        ..., description="Scale denominator of this tile matrix"
    )
    cellSize: float = Field(..., description="Cell size of this tile matrix")
    cornerOfOrigin: Optional[Literal["topLeft", "bottomLeft"]] = Field(
        description="The corner of the tile matrix (_topLeft_ or _bottomLeft_) used as the origin for numbering tile rows and columns. This corner is also a corner of the (0, 0) tile."
    )
    pointOfOrigin: BoundsType = Field(
        ...,
        description="Precise position in CRS coordinates of the corner of origin (e.g. the top-left corner) for this tile matrix. This position is also a corner of the (0, 0) tile. In previous version, this was 'topLeftCorner' and 'cornerOfOrigin' did not exist.",
    )
    tileWidth: int = Field(
        ...,
        ge=1,
        multiple_of=1,
        description="Width of each tile of this tile matrix in pixels",
    )
    tileHeight: int = Field(
        ...,
        ge=1,
        multiple_of=1,
        description="Height of each tile of this tile matrix in pixels",
    )
    matrixWidth: int = Field(
        ...,
        ge=1,
        multiple_of=1,
        description="Width of the matrix (number of tiles in width)",
    )
    matrixHeight: int = Field(
        ...,
        ge=1,
        multiple_of=1,
        description="Height of the matrix (number of tiles in height)",
    )
    # variableMatrixWidths: Optional[List[variableMatrixWidth]] = Field(description="Describes the rows that has variable matrix width")

    class Config:
        """Forbid additional items like variableMatrixWidths."""

        extra = "forbid"


class TileMatrixSet(BaseModel):
    """Tile Matrix Set Definition

    A definition of a tile matrix set following the Tile Matrix Set standard.
    For tileset metadata, such a description (in `tileMatrixSet` property) is only required for offline use,
    as an alternative to a link with a `http://www.opengis.net/def/rel/ogc/1.0/tiling-scheme` relation type.

    ref: https://github.com/opengeospatial/2D-Tile-Matrix-Set/blob/master/schemas/tms/2.0/json/tileMatrixSet.json

    """

    title: Optional[str] = Field(
        description="Title of this tile matrix set, normally used for display to a human"
    )
    description: Optional[str] = Field(
        description="Brief narrative description of this tile matrix set, normally available for display to a human"
    )
    keywords: Optional[List[str]] = Field(
        description="Unordered list of one or more commonly used or formalized word(s) or phrase(s) used to describe this tile matrix set"
    )
    id: Optional[str] = Field(
        regex=r"^[\w\d_\-]+$",
        description="Tile matrix set identifier. Implementation of 'identifier'",
    )
    uri: Optional[str] = Field(
        description="Reference to an official source for this tileMatrixSet"
    )
    orderedAxes: Optional[axesInfo]
    crs: CRSType = Field(..., description="Coordinate Reference System (CRS)")
    wellKnownScaleSet: Optional[AnyHttpUrl] = Field(
        description="Reference to a well-known scale set"
    )
    boundingBox: Optional[TMSBoundingBox] = Field(
        description="Minimum bounding rectangle surrounding the tile matrix set, in the supported CRS"
    )
    tileMatrices: List[TileMatrix] = Field(
        ..., description="Describes scale levels and its tile matrices"
    )

    # Private attributes
    _is_quadtree: bool = PrivateAttr()
    _geographic_crs: CRS = PrivateAttr(default=WGS84_CRS)
    _to_geographic: Transformer = PrivateAttr()
    _from_geographic: Transformer = PrivateAttr()

    class Config:
        """Configure TileMatrixSet."""

        arbitrary_types_allowed = True

    def __init__(self, **data):
        """Create PyProj transforms and check if TileMatrixSet supports quadkeys."""
        if {"supportedCRS", "topLeftCorner"}.intersection(data):
            raise DeprecationError(
                "Tile Matrix Set must be version 2.0. Use morecantile <4.0 for TMS 1.0 support"
            )

        super().__init__(**data)

        self._is_quadtree = check_quadkey_support(self.tileMatrices)
        self._geographic_crs = data.get("_geographic_crs", WGS84_CRS)

        try:
            self._to_geographic = Transformer.from_crs(
                self.crs._pyproj_crs, self._geographic_crs, always_xy=True
            )
            self._from_geographic = Transformer.from_crs(
                self._geographic_crs, self.crs._pyproj_crs, always_xy=True
            )
        except ProjError:
            warnings.warn(
                "Could not create coordinate Transformer from input CRS to the given geographic CRS"
                "some methods might not be available.",
                UserWarning,
            )
            self._to_geographic = None
            self._from_geographic = None

    @validator("tileMatrices")
    def sort_tile_matrices(cls, v):
        """Sort matrices by identifier"""
        return sorted(v, key=lambda m: int(m.id))

    def __iter__(self):
        """Iterate over matrices"""
        for matrix in self.tileMatrices:
            yield matrix

    def __repr__(self):
        """Simplify default pydantic model repr."""
        return f"<TileMatrixSet title='{self.title}' id='{self.id}' crs='{self.crs.__root__}>"

    @property
    def geographic_crs(self) -> CRSType:
        """Return the TMS's geographic CRS."""
        return self._geographic_crs

    @property
    def rasterio_crs(self):
        """Return rasterio CRS."""
        return to_rasterio_crs(self.crs._pyproj_crs)

    @property
    def rasterio_geographic_crs(self):
        """Return the geographic CRS as a rasterio CRS."""
        return to_rasterio_crs(self._geographic_crs)

    @property
    def minzoom(self) -> int:
        """TileMatrixSet minimum TileMatrix identifier"""
        return int(self.tileMatrices[0].id)

    @property
    def maxzoom(self) -> int:
        """TileMatrixSet maximum TileMatrix identifier"""
        return int(self.tileMatrices[-1].id)

    @property
    def _invert_axis(self) -> bool:
        """Check if CRS has inverted AXIS (lat,lon) instead of (lon,lat)."""
        return (
            ordered_axis_inverted(self.orderedAxes)
            if self.orderedAxes
            else crs_axis_inverted(self.crs._pyproj_crs)
        )

    @classmethod
    def from_v1(cls, tms: Dict) -> "TileMatrixSet":
        """
        Makes a TMS from a v1 TMS definition

                Attributes
        ----------
        supportedCRS: CRSType
            Tile Matrix Set coordinate reference system
        title: str
            Title of TMS
        abstract: str (optional)
            Abstract of CRS
        keywords: str (optional)
            Keywords
        identifier: str
            TMS Identifier
        wellKnownScaleSet: AnyHttpUrl (optional)
            WKSS URL
        boundingBox: TMSBoundingBox (optional)
            Bounding box of TMS
        tileMatrix: List[TileMatrix]
            List of Tile Matrices

        Returns:
        --------
        TileMatrixSet
        """
        v2_tms = tms.copy()

        del v2_tms["type"]

        if tms_bbox := v2_tms.pop("boundingBox", None):
            del tms_bbox["type"]
            tms_bbox["lowerLeft"] = tms_bbox.pop("lowerCorner")
            tms_bbox["upperRight"] = tms_bbox.pop("upperCorner")
            v2_tms["boundingBox"] = tms_bbox

        v2_tms["crs"] = v2_tms.pop("supportedCRS")
        v2_tms["tileMatrices"] = v2_tms.pop("tileMatrix")
        v2_tms["id"] = v2_tms.pop("identifier")
        mpu = meters_per_unit(CRS.from_user_input(v2_tms["crs"]))
        for i in range(len(v2_tms["tileMatrices"])):
            v2_tms["tileMatrices"][i]["cellSize"] = (
                v2_tms["tileMatrices"][i]["scaleDenominator"] * 0.00028 / mpu
            )
            v2_tms["tileMatrices"][i]["pointOfOrigin"] = v2_tms["tileMatrices"][i].pop(
                "topLeftCorner"
            )
            v2_tms["tileMatrices"][i]["id"] = v2_tms["tileMatrices"][i].pop(
                "identifier"
            )
            del v2_tms["tileMatrices"][i]["type"]

        return TileMatrixSet(**v2_tms)

    @classmethod
    def custom(
        cls,
        extent: List[float],
        crs: CRS,
        tile_width: int = 256,
        tile_height: int = 256,
        matrix_scale: Optional[List] = None,
        extent_crs: Optional[CRS] = None,
        minzoom: int = 0,
        maxzoom: int = 24,
        title: Optional[str] = None,
        id: Optional[str] = None,
        ordered_axes: Optional[List[str]] = None,
        geographic_crs: CRS = WGS84_CRS,
        **kwargs: Any,
    ):
        """
        Construct a custom TileMatrixSet.

        Attributes
        ----------
        crs: pyproj.CRS
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
        extent_crs: pyproj.CRS
            Extent's coordinate reference system, as a pyproj CRS object.
            (default: same as input crs)
        minzoom: int
            Tile Matrix Set minimum zoom level (default is 0).
        maxzoom: int
            Tile Matrix Set maximum zoom level (default is 24).
        title: str, optional
            Tile Matrix Set title
        id: str, optional
            Tile Matrix Set identifier
        geographic_crs: pyproj.CRS
            Geographic (lat,lon) coordinate reference system (default is EPSG:4326)
        kwargs: Any
            Attributes to forward to the TileMatrixSet

        Returns:
        --------
        TileMatrixSet

        """
        matrix_scale = matrix_scale or [1, 1]

        if ordered_axes:
            is_inverted = ordered_axis_inverted(ordered_axes)
        else:
            is_inverted = crs_axis_inverted(crs)

        if extent_crs:
            transform = Transformer.from_crs(extent_crs, crs, always_xy=True)
            extent = transform.transform_bounds(*extent, densify_pts=21)

        bbox = BoundingBox(*extent)
        x_origin = bbox.left if not is_inverted else bbox.top
        y_origin = bbox.top if not is_inverted else bbox.left
        width = abs(bbox.right - bbox.left)
        height = abs(bbox.top - bbox.bottom)
        mpu = meters_per_unit(crs)

        tile_matrices: List[TileMatrix] = []
        for zoom in range(minzoom, maxzoom + 1):
            res = max(
                width / (tile_width * matrix_scale[0]) / 2.0**zoom,
                height / (tile_height * matrix_scale[1]) / 2.0**zoom,
            )
            tile_matrices.append(
                TileMatrix(
                    **{
                        "id": str(zoom),
                        "scaleDenominator": res * mpu / 0.00028,
                        "cellSize": res,
                        "pointOfOrigin": [x_origin, y_origin],
                        "tileWidth": tile_width,
                        "tileHeight": tile_height,
                        "matrixWidth": matrix_scale[0] * 2**zoom,
                        "matrixHeight": matrix_scale[1] * 2**zoom,
                    }
                )
            )

        if crs.to_authority(min_confidence=20):
            crs_str = CRS_to_uri(crs)

            # Some old Proj version might not support URI
            # so we fall back to wkt
            try:
                CRS.from_user_input(crs_str)
            except CRSError:
                crs_str = crs.to_wkt()

        else:
            crs_str = crs.to_wkt()

        return cls(
            crs=crs_str,
            tileMatrices=tile_matrices,
            id=id,
            title=title,
            _geographic_crs=geographic_crs,
            **kwargs,
        )

    def matrix(self, zoom: int) -> TileMatrix:
        """Return the TileMatrix for a specific zoom."""
        for m in self.tileMatrices:
            if m.id == str(zoom):
                return m

        matrix_scale = list(
            {
                round(
                    self.tileMatrices[idx].scaleDenominator
                    / self.tileMatrices[idx - 1].scaleDenominator,
                    2,
                )
                for idx in range(1, len(self.tileMatrices))
            }
        )
        if len(matrix_scale) > 1:
            raise InvalidZoomError(
                f"TileMatrix not found for level: {zoom} - Unable to construct tileMatrix for TMS with variable scale"
            )

        warnings.warn(
            f"TileMatrix not found for level: {zoom} - Creating values from TMS Scale.",
            UserWarning,
        )

        tile_matrix = self.tileMatrices[-1]
        factor = 1 / matrix_scale[0]
        while not str(zoom) == tile_matrix.id:
            tile_matrix = TileMatrix(
                **{
                    "id": str(int(tile_matrix.id) + 1),
                    "scaleDenominator": tile_matrix.scaleDenominator / factor,
                    "cellSize": tile_matrix.cellSize / factor,
                    "pointOfOrigin": tile_matrix.pointOfOrigin,
                    "tileWidth": tile_matrix.tileWidth,
                    "tileHeight": tile_matrix.tileHeight,
                    "matrixWidth": int(tile_matrix.matrixWidth * factor),
                    "matrixHeight": int(tile_matrix.matrixHeight * factor),
                }
            )

        return tile_matrix

    def _resolution(self, matrix: TileMatrix) -> float:
        """
        Tile resolution for a TileMatrix.

        From note g in http://docs.opengeospatial.org/is/17-083r2/17-083r2.html#table_2:
          The pixel size of the tile can be obtained from the scaleDenominator
          by multiplying the later by 0.28 10-3 / metersPerUnit.

        """
        return matrix.scaleDenominator * 0.28e-3 / meters_per_unit(self.crs._pyproj_crs)

    def zoom_for_res(
        self,
        res: float,
        max_z: Optional[int] = None,
        zoom_level_strategy: str = "auto",
        min_z: Optional[int] = None,
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
            min_z (int): Minimum zoom level (default is tms minzoom).

        Returns:
            int: TMS zoom for a given resolution.

        Examples:
            >>> zoom_for_res(430.021)

        """
        if max_z is None:
            max_z = self.maxzoom

        if min_z is None:
            min_z = self.minzoom

        # Freely adapted from https://github.com/OSGeo/gdal/blob/dc38aa64d779ecc45e3cd15b1817b83216cf96b8/gdal/frmts/gtiff/cogdriver.cpp#L272-L305
        for zoom_level in range(min_z, max_z + 1):
            matrix_res = self._resolution(self.matrix(zoom_level))
            if res > matrix_res or abs(res - matrix_res) / matrix_res <= 1e-8:
                break

        if zoom_level > 0 and abs(res - matrix_res) / matrix_res > 1e-8:
            if zoom_level_strategy.lower() == "lower":
                zoom_level = max(zoom_level - 1, min_z)
            elif zoom_level_strategy.lower() == "upper":
                zoom_level = min(zoom_level, max_z)
            elif zoom_level_strategy.lower() == "auto":
                if (self._resolution(self.matrix(max(zoom_level - 1, min_z))) / res) < (
                    res / matrix_res
                ):
                    zoom_level = max(zoom_level - 1, min_z)
            else:
                raise ValueError(
                    f"Invalid strategy: {zoom_level_strategy}. Should be one of lower|upper|auto"
                )

        return zoom_level

    def lnglat(self, x: float, y: float, truncate=False) -> Coords:
        """Transform point(x,y) to geographic longitude and latitude."""
        inside = point_in_bbox(Coords(x, y), self.xy_bbox)
        if not inside:
            warnings.warn(
                f"Point ({x}, {y}) is outside TMS bounds {list(self.xy_bbox)}.",
                PointOutsideTMSBounds,
            )

        lng, lat = self._to_geographic.transform(x, y)

        if truncate:
            lng, lat = self.truncate_lnglat(lng, lat)

        return Coords(lng, lat)

    def xy(self, lng: float, lat: float, truncate=False) -> Coords:
        """Transform geographic longitude and latitude coordinates to TMS CRS."""
        if truncate:
            lng, lat = self.truncate_lnglat(lng, lat)

        inside = point_in_bbox(Coords(lng, lat), self.bbox)
        if not inside:
            warnings.warn(
                f"Point ({lng}, {lat}) is outside TMS bounds {list(self.bbox)}.",
                PointOutsideTMSBounds,
            )

        x, y = self._from_geographic.transform(lng, lat)

        return Coords(x, y)

    def truncate_lnglat(self, lng: float, lat: float) -> Tuple[float, float]:
        """
        Truncate geographic coordinates to TMS geographic bbox.

        Adapted from https://github.com/mapbox/mercantile/blob/master/mercantile/__init__.py

        """
        if lng > self.bbox.right:
            lng = self.bbox.right
        elif lng < self.bbox.left:
            lng = self.bbox.left

        if lat > self.bbox.top:
            lat = self.bbox.top
        elif lat < self.bbox.bottom:
            lat = self.bbox.bottom

        return lng, lat

    def _tile(self, xcoord: float, ycoord: float, zoom: int) -> Tile:
        """
        Get the tile containing a Point (in TMS CRS).

        Parameters
        ----------
        xcoord, ycoord : float
            A `X` and `Y` pair in TMS coordinate reference system.
        zoom : int
            The zoom level.

        Returns
        -------
        Tile

        """
        matrix = self.matrix(zoom)
        res = self._resolution(matrix)

        origin_x = (
            matrix.pointOfOrigin[1] if self._invert_axis else matrix.pointOfOrigin[0]
        )
        origin_y = (
            matrix.pointOfOrigin[0] if self._invert_axis else matrix.pointOfOrigin[1]
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
        Get the tile for a given geographic longitude and latitude pair.

        Parameters
        ----------
        lng, lat : float
            A longitude and latitude pair in geographic coordinate reference system.
        zoom : int
            The zoom level.
        truncate : bool
            Whether or not to truncate inputs to limits of TMS geographic bounds.

        Returns
        -------
        Tile

        """
        x, y = self.xy(lng, lat, truncate=truncate)
        return self._tile(x, y, zoom)

    def _ul(self, *tile: Tile) -> Coords:
        """
        Return the upper left coordinate of the tile in TMS coordinate reference system.

        Attributes
        ----------
        tile: (x, y, z) tile coordinates or a Tile object we want the upper left coordinates of.

        Returns
        -------
        Coords: The upper left coordinates of the input tile.

        """
        t = _parse_tile_arg(*tile)

        matrix = self.matrix(t.z)
        res = self._resolution(matrix)

        origin_x = (
            matrix.pointOfOrigin[1] if self._invert_axis else matrix.pointOfOrigin[0]
        )
        origin_y = (
            matrix.pointOfOrigin[0] if self._invert_axis else matrix.pointOfOrigin[1]
        )

        xcoord = origin_x + t.x * res * matrix.tileWidth
        ycoord = origin_y - t.y * res * matrix.tileHeight
        return Coords(xcoord, ycoord)

    def xy_bounds(self, *tile: Tile) -> BoundingBox:
        """
        Return the bounding box of the tile in TMS coordinate reference system.

        Attributes
        ----------
        tile: A tuple of (x, y, z) tile coordinates or a Tile object we want the bounding box of.

        Returns
        -------
        BoundingBox: The bounding box of the input tile.

        """
        t = _parse_tile_arg(*tile)

        left, top = self._ul(t)
        right, bottom = self._ul(Tile(t.x + 1, t.y + 1, t.z))
        return BoundingBox(left, bottom, right, top)

    def ul(self, *tile: Tile) -> Coords:
        """
        Return the upper left coordinates of the tile in geographic coordinate reference system.

        Attributes
        ----------
        tile (tuple or Tile): (x, y, z) tile coordinates or a Tile object we want the upper left geographic coordinates of.

        Returns
        -------
        Coords: The upper left geographic coordinates of the input tile.

        """
        t = _parse_tile_arg(*tile)

        x, y = self._ul(t)
        return Coords(*self.lnglat(x, y))

    def bounds(self, *tile: Tile) -> BoundingBox:
        """
        Return the bounding box of the tile in geographic coordinate reference system.

        Attributes
        ----------
        tile (tuple or Tile): A tuple of (x, y, z) tile coordinates or a Tile object we want the bounding box of.

        Returns
        -------
        BoundingBox: The bounding box of the input tile.

        """
        t = _parse_tile_arg(*tile)

        left, top = self.ul(t)
        right, bottom = self.ul(Tile(t.x + 1, t.y + 1, t.z))
        return BoundingBox(left, bottom, right, top)

    @property
    def xy_bbox(self):
        """Return TMS bounding box in TileMatrixSet's CRS."""
        zoom = self.minzoom
        matrix = self.matrix(zoom)

        left, top = self._ul(Tile(0, 0, zoom))
        right, bottom = self._ul(Tile(matrix.matrixWidth, matrix.matrixHeight, zoom))

        return BoundingBox(left, bottom, right, top)

    @property
    @cached(  # type: ignore
        LRUCache(maxsize=512),
        key=lambda self: hashkey(
            self.crs.__root__,
            self.tileMatrices[0].pointOfOrigin,
            self.tileMatrices[0].matrixWidth,
            self.tileMatrices[0].matrixHeight,
        ),
    )
    def bbox(self):
        """Return TMS bounding box in geographic coordinate reference system."""
        left, bottom, right, top = self.xy_bbox
        return BoundingBox(
            *self._to_geographic.transform_bounds(
                left,
                bottom,
                right,
                top,
                densify_pts=21,
            )
        )

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
            Bounding values in decimal degrees (geographic CRS).
        zooms : int or sequence of int
            One or more zoom levels.
        truncate : bool, optional
            Whether or not to truncate inputs to TMS limits.

        Yields
        ------
        Tile

        Notes
        -----
        A small epsilon is used on the south and east parameters so that this
        function yields exactly one tile when given the bounds of that same tile.

        """
        if any(math.isnan(coord) for coord in (west, south, east, north)):
            raise ValueError("All coordinates must be finite")

        if isinstance(zooms, int):
            zooms = (zooms,)

        if truncate:
            west, south = self.truncate_lnglat(west, south)
            east, north = self.truncate_lnglat(east, north)

        if west > east:
            bbox_west = (self.bbox.left, south, east, north)
            bbox_east = (west, south, self.bbox.right, north)
            bboxes = [bbox_west, bbox_east]
        else:
            bboxes = [(west, south, east, north)]

        for w, s, e, n in bboxes:
            # Clamp bounding values.
            w = max(self.bbox.left, w)
            s = max(self.bbox.bottom, s)
            e = min(self.bbox.right, e)
            n = min(self.bbox.top, n)

            for z in zooms:
                nw_tile = self.tile(
                    w + LL_EPSILON, n - LL_EPSILON, z
                )  # Not in mercantile
                se_tile = self.tile(e - LL_EPSILON, s + LL_EPSILON, z)

                minx = min(nw_tile.x, se_tile.x)
                maxx = max(nw_tile.x, se_tile.x)
                miny = min(nw_tile.y, se_tile.y)
                maxy = max(nw_tile.y, se_tile.y)

                for i in range(minx, maxx + 1):
                    for j in range(miny, maxy + 1):
                        yield Tile(i, j, z)

    def feature(
        self,
        tile: Tile,
        fid: Optional[str] = None,
        props: Optional[Dict] = None,
        buffer: Optional[NumType] = None,
        precision: Optional[int] = None,
        projected: bool = False,
    ) -> Dict:
        """
        Get the GeoJSON feature corresponding to a tile.

        Originally from https://github.com/mapbox/mercantile/blob/master/mercantile/__init__.py

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
            west, south, east, north = self._to_geographic.transform_bounds(
                west, south, east, north, densify_pts=21
            )

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
                "grid_name": self.id,
                "grid_crs": self.crs.__root__,
            },
        }

        if projected:
            warnings.warn(
                "CRS is no longer part of the GeoJSON specification."
                "Other projection than EPSG:4326 might not be supported.",
                UserWarning,
            )
            feat.update(
                {
                    "crs": {
                        "type": "EPSG",
                        "properties": {"code": self.crs.to_epsg()},
                    }
                }
            )

        if props:
            feat["properties"].update(props)

        if fid is not None:
            feat["id"] = fid

        return feat

    def quadkey(self, *tile: Tile) -> str:
        """Get the quadkey of a tile

        Parameters
        ----------
        tile : Tile or sequence of int
            May be be either an instance of Tile or 3 ints, X, Y, Z.

        Returns
        -------
        str

        """
        if not self._is_quadtree:
            raise NoQuadkeySupport(
                "This Tile Matrix Set doesn't support 2 x 2 quadkeys."
            )

        t = _parse_tile_arg(*tile)

        qk = []
        for z in range(t.z, self.minzoom, -1):
            digit = 0
            mask = 1 << (z - 1)
            if t.x & mask:
                digit += 1
            if t.y & mask:
                digit += 2
            qk.append(str(digit))

        return "".join(qk)

    def quadkey_to_tile(self, qk: str) -> Tile:
        """Get the tile corresponding to a quadkey

        Parameters
        ----------
        qk : str
            A quadkey string.

        Returns
        -------
        Tile

        """
        if not self._is_quadtree:
            raise NoQuadkeySupport(
                "This Tile Matrix Set doesn't support 2 x 2 quadkeys."
            )

        if len(qk) == 0:
            return Tile(0, 0, 0)

        xtile, ytile = 0, 0
        for i, digit in enumerate(reversed(qk)):
            mask = 1 << i
            if digit == "1":
                xtile = xtile | mask
            elif digit == "2":
                ytile = ytile | mask
            elif digit == "3":
                xtile = xtile | mask
                ytile = ytile | mask
            elif digit != "0":
                raise QuadKeyError("Unexpected quadkey digit: %r", digit)

        return Tile(xtile, ytile, i + 1)

    def minmax(self, zoom: int) -> Dict:
        """Return TileMatrix Extrema.

        Parameters
        ----------
        zoom : int
            The zoom level.

        Returns
        -------
        Dict

        """
        m = self.matrix(zoom)
        return {
            "x": {"min": 0, "max": m.matrixWidth - 1},
            "y": {"min": 0, "max": m.matrixHeight - 1},
        }

    def is_valid(self, *tile: Tile) -> bool:
        """Check if a tile is valid."""
        t = _parse_tile_arg(*tile)

        if t.z < self.minzoom:
            return False

        extrema = self.minmax(t.z)
        validx = extrema["x"]["min"] <= t.x <= extrema["x"]["max"]
        validy = extrema["y"]["min"] <= t.y <= extrema["y"]["max"]

        return validx and validy

    def neighbors(self, *tile: Tile) -> List[Tile]:
        """The neighbors of a tile

        The neighbors function makes no guarantees regarding neighbor tile
        ordering.

        The neighbors function returns up to eight neighboring tiles, where
        tiles will be omitted when they are not valid.

        Parameters
        ----------
        tile : Tile or sequence of int
            May be be either an instance of Tile or 3 ints, X, Y, Z.

        Returns
        -------
        list

        """
        t = _parse_tile_arg(*tile)
        extrema = self.minmax(t.z)

        tiles = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                elif t.x + i < extrema["x"]["min"] or t.y + j < extrema["y"]["min"]:
                    continue

                elif t.x + i > extrema["x"]["max"] or t.y + j > extrema["y"]["max"]:
                    continue

                tiles.append(Tile(x=t.x + i, y=t.y + j, z=t.z))

        return tiles

    def parent(self, *tile: Tile, zoom: int = None):
        """Get the parent of a tile

        The parent is the tile of one zoom level lower that contains the
        given "child" tile.

        Parameters
        ----------
        tile : Tile or sequence of int
            May be be either an instance of Tile or 3 ints, X, Y, Z.
        zoom : int, optional
            Determines the *zoom* level of the returned parent tile.
            This defaults to one lower than the tile (the immediate parent).

        Returns
        -------
        list: list of Tile

        """
        t = _parse_tile_arg(*tile)

        if t.z == self.minzoom:
            return []

        if zoom is not None and t.z <= zoom:
            raise InvalidZoomError("zoom must be less than that of the input tile")

        target_zoom = t.z - 1 if zoom is None else zoom

        res = self._resolution(self.matrix(t.z)) / 10.0

        bbox = self.xy_bounds(t)
        ul_tile = self._tile(bbox.left + res, bbox.top - res, target_zoom)
        lr_tile = self._tile(bbox.right - res, bbox.bottom + res, target_zoom)

        tiles = []
        for i in range(ul_tile.x, lr_tile.x + 1):
            for j in range(ul_tile.y, lr_tile.y + 1):
                tiles.append(Tile(i, j, target_zoom))

        return tiles

    def children(self, *tile: Tile, zoom: int = None):
        """Get the children of a tile

        The children are ordered: top-left, top-right, bottom-right, bottom-left.

        Parameters
        ----------
        tile : Tile or sequence of int
            May be be either an instance of Tile or 3 ints, X, Y, Z.
        zoom : int, optional
            Determines the *zoom* level of the returned child tiles.
            This defaults to one higher than the tile (the immediate children).

        Returns
        -------
        list: list of Tile

        """
        t = _parse_tile_arg(*tile)

        if zoom is not None and t.z > zoom:
            raise InvalidZoomError("zoom must be greater than that of the input tile")

        target_zoom = t.z + 1 if zoom is None else zoom

        bbox = self.xy_bounds(t)
        res = self._resolution(self.matrix(t.z)) / 10.0

        ul_tile = self._tile(bbox.left + res, bbox.top - res, target_zoom)
        lr_tile = self._tile(bbox.right - res, bbox.bottom + res, target_zoom)

        tiles = []
        for i in range(ul_tile.x, lr_tile.x + 1):
            for j in range(ul_tile.y, lr_tile.y + 1):
                tiles.append(Tile(i, j, target_zoom))

        return tiles
