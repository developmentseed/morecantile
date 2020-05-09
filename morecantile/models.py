"""Pydantic modules for OGC TileMatrixSets (https://www.ogc.org/standards/tms)"""
from typing import List, Optional, Tuple, Union

from pydantic import BaseModel, Field


NumType = Union[float, int]
BoundsType = Tuple[NumType, NumType]


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
    supportedCRS: str = Field(..., regex=r"^http")
    wellKnownScaleSet: Optional[str] = Field(None, regex=r"^http")
    boundingBox: Optional[BoundingBox]
    tileMatrix: List[TileMatrix]
