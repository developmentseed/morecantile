"""Default Morecantile TMS."""

import os
import pathlib
from copy import copy, deepcopy

import attr

from morecantile.errors import InvalidIdentifier
from morecantile.models import TileMatrixSet

morecantile_tms_dir = pathlib.Path(__file__).parent.joinpath("data")
tms_paths = list(pathlib.Path(morecantile_tms_dir).glob("*.json"))

user_tms_dir = os.environ.get("TILEMATRIXSET_DIRECTORY", None)
if user_tms_dir:
    tms_paths.extend(list(pathlib.Path(user_tms_dir).glob("*.json")))

default_tms: dict[str, TileMatrixSet | pathlib.Path] = {
    tms.stem: tms for tms in sorted(tms_paths)
}


@attr.s(frozen=True)
class TileMatrixSets:
    """Default TileMatrixSets holder."""

    tilematrixsets: dict = attr.ib()

    def get(self, identifier: str) -> TileMatrixSet:
        """Fetch a TMS."""
        if identifier not in self.tilematrixsets:
            raise InvalidIdentifier(f"Invalid identifier: {identifier}")

        tilematrix = self.tilematrixsets[identifier]

        # We lazyload the TMS document only when called
        if isinstance(tilematrix, pathlib.Path):
            with tilematrix.open() as f:
                tilematrix = TileMatrixSet.model_validate_json(f.read())
                self.tilematrixsets[identifier] = tilematrix

        return deepcopy(tilematrix)

    def list(self) -> list[str]:
        """List registered TMS."""
        return list(self.tilematrixsets.keys())

    def register(
        self,
        custom_tms: dict[str, TileMatrixSet],
        overwrite: bool = False,
    ) -> "TileMatrixSets":
        """Register TileMatrixSet(s)."""
        for identifier in custom_tms.keys():
            if identifier in self.tilematrixsets and not overwrite:
                raise InvalidIdentifier(f"{identifier} is already a registered TMS.")

        return TileMatrixSets({**self.tilematrixsets, **custom_tms})


tms = TileMatrixSets(copy(default_tms))  # noqa
