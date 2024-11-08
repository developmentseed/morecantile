"""Morecantile errors."""


class MorecantileError(Exception):
    """Base error for Morecantile."""


class InvalidIdentifier(MorecantileError):
    """Invalid TileMatrixSet indentifier."""


class InvalidLatitudeError(MorecantileError):
    """Raised when math errors occur beyond ~85 degrees N or S"""


class TileArgParsingError(MorecantileError):
    """Raised when errors occur in parsing a function's tile arg(s)"""


class PointOutsideTMSBounds(UserWarning):
    """Point is outside TMS bounds."""


class NoQuadkeySupport(MorecantileError):
    """Raised when a custom TileMatrixSet doesn't support quadkeys"""


class QuadKeyError(MorecantileError):
    """Raised when errors occur in computing or parsing quad keys"""


class InvalidZoomError(MorecantileError):
    """Raised when input zoom is invalid."""


class DeprecationError(MorecantileError):
    """Raised when TMS version is not 2.0"""


class NonWGS84GeographicCRS(UserWarning):
    """Geographic CRS is not EPSG:4326."""
