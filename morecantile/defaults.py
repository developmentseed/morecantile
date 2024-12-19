"""Default Morecantile TMS."""

import os
import pathlib
from copy import copy
from typing import Dict, List, Union

import attr

from morecantile.errors import InvalidIdentifier
from morecantile.models import TileMatrixSet

morecantile_tms_dir = pathlib.Path(__file__).parent.joinpath("data")
tms_paths = list(pathlib.Path(morecantile_tms_dir).glob("*.json"))

user_tms_dir = os.environ.get("TILEMATRIXSET_DIRECTORY", None)
if user_tms_dir:
    tms_paths.extend(list(pathlib.Path(user_tms_dir).glob("*.json")))

default_tms: Dict[str, Union[TileMatrixSet, pathlib.Path]] = {
    tms.stem: tms for tms in sorted(tms_paths)
}


@attr.s(frozen=True)
class TileMatrixSets:
    """Default TileMatrixSets holder."""

    tms: Dict = attr.ib()

    def get(self, identifier: str) -> TileMatrixSet:
        """Fetch a TMS."""
        if identifier not in self.tms:
            raise InvalidIdentifier(f"Invalid identifier: {identifier}")

        tms = self.tms[identifier]

        # We lazyload the TMS document only when called
        if isinstance(tms, pathlib.Path):
            with tms.open() as f:
                tms = TileMatrixSet.model_validate_json(f.read())
                self.tms[identifier] = tms

        return tms

    def list(self) -> List[str]:
        """List registered TMS."""
        return list(self.tms.keys())

    def register(
        self,
        custom_tms: Dict[str, TileMatrixSet],
        overwrite: bool = False,
    ) -> "TileMatrixSets":
        """Register TileMatrixSet(s)."""
        for identifier in custom_tms.keys():
            if identifier in self.tms and not overwrite:
                raise InvalidIdentifier(f"{identifier} is already a registered TMS.")

        return TileMatrixSets({**self.tms, **custom_tms})


tms = TileMatrixSets(copy(default_tms))  # noqa
