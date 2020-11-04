"""Default Morecantile TMS."""

import os
import pathlib
from copy import deepcopy
from typing import Dict, List, Sequence, Union

import attr

from .errors import InvalidIdentifier
from .models import TileMatrixSet

morecantile_tms_dir = pathlib.Path(__file__).parent.joinpath("data")
tms_paths = list(pathlib.Path(morecantile_tms_dir).glob("*.json"))

user_tms_dir = os.environ.get("TILEMATRIXSET_DIRECTORY", None)
if user_tms_dir:
    tms_paths.extend(list(pathlib.Path(user_tms_dir).glob("*.json")))

default_tms: Dict[str, TileMatrixSet] = {
    tms.stem: TileMatrixSet.parse_file(tms) for tms in tms_paths
}


@attr.s(frozen=True)
class TileMatrixSets:
    """Default TileMatrixSets holder."""

    tms: Dict = attr.ib()

    def get(self, identifier: str) -> TileMatrixSet:
        """Fetch a TMS."""
        if identifier not in self.tms:
            raise InvalidIdentifier(f"Invalid identifier: {identifier}")

        return self.tms[identifier]

    def list(self) -> List[str]:
        """List registered TMS."""
        return list(self.tms.keys())

    def register(
        self,
        custom_tms: Union[TileMatrixSet, Sequence[TileMatrixSet]],
        overwrite: bool = False,
    ) -> "TileMatrixSets":
        """Register TileMatrixSet(s)."""
        if isinstance(custom_tms, TileMatrixSet):
            custom_tms = (custom_tms,)

        for tms in custom_tms:
            if tms.identifier in self.tms and not overwrite:
                raise Exception(f"{tms.identifier} is already a registered TMS.")

        new_tms = {tms.identifier: tms for tms in custom_tms}
        return TileMatrixSets({**self.tms, **new_tms})


tms = TileMatrixSets(deepcopy(default_tms))  # noqa
