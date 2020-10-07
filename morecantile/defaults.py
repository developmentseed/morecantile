"""Default Morecantile TMS."""

import os
import pathlib
from typing import Dict, List

from .errors import InvalidIdentifier
from .models import TileMatrixSet

morecantile_tms_dir = pathlib.Path(__file__).parent.joinpath("data")
user_tms_dir = os.environ.get("TILEMATRIXSET_DIRECTORY", None)


class DefaultTileMatrixSets(object):
    """Default TileMatrixSets holder."""

    def __init__(self):
        """Load default TMS in a dict."""

        tms_paths = list(pathlib.Path(morecantile_tms_dir).glob("*.json"))
        if user_tms_dir:
            tms_paths.extend(list(pathlib.Path(user_tms_dir).glob("*.json")))

        self._data: Dict[str, TileMatrixSet] = {
            tms.stem: TileMatrixSet.parse_file(tms) for tms in tms_paths
        }

    def get(self, identifier: str) -> TileMatrixSet:
        """Fetch a TMS."""
        if identifier not in self._data:
            raise InvalidIdentifier(f"Invalid identifier: {identifier}")

        return self._data[identifier]

    def list(self) -> List[str]:
        """List registered TMS."""
        return list(self._data.keys())

    def register(self, custom_tms: TileMatrixSet):
        """Register a custom TileMatrixSet."""
        self._data[custom_tms.identifier] = custom_tms


tms = DefaultTileMatrixSets()  # noqa
