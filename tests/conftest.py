import os.path
import pathlib

import pytest

from morecantile import tms


@pytest.fixture(scope="session", autouse=True)
def register_WebMercatorQuadBottomLeft():
    """Automatically load in WebMercatorQuadBottomLeft once as the start of the testing session"""
    directory = os.path.split(__file__)[0]
    file_path = os.path.join(
        directory, "fixtures", "bottomLeft_tms", "WebMercatorQuadBottomLeft.json"
    )
    path_obj = pathlib.Path(file_path)
    tms.tms["WebMercatorQuadBottomLeft"] = path_obj
    # Load
    tms.get("WebMercatorQuadBottomLeft")
