"""Default Morecantile TMS."""

import os
from typing import List

from .errors import InvalidIdentifier
from .models import TileMatrixSet

data_dir = os.path.join(os.path.dirname(__file__), "data")


class DefaultTileMatrixSets(object):
    """Default TileMatrixSets holder."""

    def __init__(self):
        """Load default TMS in a dict."""
        default_grids = [
            os.path.splitext(f)[0] for f in os.listdir(data_dir) if f.endswith(".json")
        ]

        self._data = {
            grid: TileMatrixSet.parse_file(os.path.join(data_dir, f"{grid}.json"))
            for grid in default_grids
        }

    def get(self, identifier: str) -> TileMatrixSet:
        """Fetch a TMS."""
        try:
            return self._data[identifier]
        except KeyError:
            raise InvalidIdentifier(f"Invalid identifier: {identifier}")

    def list(self) -> List[str]:
        """List registered TMS."""
        return list(self._data.keys())

    def register(self, custom_tms: TileMatrixSet):
        """Register a custom TileMatrixSet."""
        self._data[custom_tms.identifier] = custom_tms


tms = DefaultTileMatrixSets()  # noqa
