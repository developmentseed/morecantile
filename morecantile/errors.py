"""Morecantile errors."""


class MorecantileError(Exception):
    """Base error for Morecantile."""


class InvalidIdentifier(MorecantileError):
    """Invalid TileMatrixSet indentifier."""


class TileArgParsingError(MorecantileError):
    """Raised when errors occur in parsing a function's tile arg(s)"""


class DeprecationWarning(UserWarning):
    """morecantile module deprecations warning."""
