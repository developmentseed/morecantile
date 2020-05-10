import json
import os

import pytest
from pydantic import ValidationError

from morecantile.models import TileMatrixSet
from rasterio.crs import CRS

data_dir = os.path.join(os.path.dirname(__file__), "../morecantile/data")
tilesets = [
    os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith(".json")
]


@pytest.mark.parametrize("tileset", tilesets)
def test_tile_matrix_set(tileset):
    # Confirm model validation is working
    ts = TileMatrixSet.parse_file(tileset)
    # This would fail if `supportedCRS` isn't valid EPSG code
    epsg = ts.crs
    isinstance(epsg, CRS)


def test_tms_not_in_epsg():
    with open(tilesets[0]) as f:
        data = json.load(f)
        # Replace supportedCRS with CRS84 which isn't defined in EPSG
        data["supportedCRS"] = "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
        with pytest.raises(ValidationError):
            TileMatrixSet(**data)
