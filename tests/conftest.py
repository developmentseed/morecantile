"""``pytest`` configuration."""

import pytest
from rasterio.env import GDALVersion

# Define helpers to skip tests based on GDAL version
gdal_version = GDALVersion.runtime()

requires_gdal_lt_3 = pytest.mark.skipif(
    gdal_version.__lt__("3.0"), reason="Requires GDAL 1.x/2.x"
)

requires_gdal3 = pytest.mark.skipif(
    not gdal_version.at_least("3.0"), reason="Requires GDAL 3.0.x"
)
