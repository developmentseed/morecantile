
## Unreleased

* remove python 3.8 support
* check `maxzoom` in `TileMatrixSet.is_valid`

    ```python
    import morecantile
    tms = morecantile.tms.get("WebMercatorQuad")

    # before
    assert tms.is_valid(0, 0, 25)
    >> UserWarning: TileMatrix not found for level: 25 - Creating values from TMS Scale.

    # now
    assert tms.is_valid(0, 0, 25), "Tile(0, 0, 25) is not valid"
    >> AssertionError: Tile(0, 0, 25) is not valid

    assert tms.is_valid(0, 0, 25, strict=False)
    >> UserWarning: TileMatrix not found for level: 25 - Creating values from TMS Scale.
    ```

## 6.2.0 (2024-12-19)

* add python 3.13 support
* update pyproj dependency version to `>=3.1,<4.0`

## 6.1.0 (2024-10-17)

* add `_tile_matrices_idx: Dict[str, int]` private attribute to improve `matrices` lookup
* change `xy_bounds()` and `bounds()` methods to avoid calculation duplication

## 6.0.0 (2024-10-16)

* remove `_geographic_crs` private attribute in `TileMatrixSet` model **breaking change**
* use `crs.geodetic_crs` property as `geographic_crs` **breaking change**

## 5.4.2 (2024-08-29)

* better handle anti-meridian crossing bbox in `tms.tiles()` (author @ljstrnadiii, https://github.com/developmentseed/morecantile/pull/154)

## 5.4.1 (2024-08-27)

* ensure `TileMatrixSet._geographic_crs` is a pyproj CRS object (author @AndrewAnnex, https://github.com/developmentseed/morecantile/pull/152)
* add `python 3.12` support

## 5.4.0 (2024-08-20)

* adds --tms optional argument to the shapes and tiles cli tools (author @AndrewAnnex, https://github.com/developmentseed/morecantile/pull/151)

## 5.3.1 (2024-07-26)

* handle 180th meridian case for `tms.tiles()` (author @ljstrnadiii, https://github.com/developmentseed/morecantile/pull/150)

## 5.3.0 (2024-02-09)

* enable custom decimation value for in `TileMatrixSet.custom` method (author @mccarthyryanc, https://github.com/developmentseed/morecantile/pull/146)

## 5.2.3 (2024-02-02)

* update pydantic `Field` usage to avoid deprecation in 3.0

## 5.2.2 (2024-01-25)

* fix `id` for `WGS1984Quad` TileMatrixSet (from `WorldCRS84Quad` to `WGS1984Quad`)

## 5.2.1 (2024-01-18)

* fix `CRS` WKT type from `string` to `Object` (PROJJSON) (ref: https://github.com/opengeospatial/2D-Tile-Matrix-Set/issues/89).

    ```python
    # Before
    wkt = pyproj.CRS.from_epsg(3857).to_wkt()
    TileMatrixSet(
        ...
        crs={"wkt": wkt}
    )

    # Now
    wkt = pyproj.CRS.from_epsg(3857).to_json_dict()
    TileMatrixSet(
        ...
        crs={"wkt": wkt}
    )
    ```

## 5.2.0 (2024-01-18)

* fix `CRS` parsing to allow `wkt ({"wkt": ...})` and `uri ({"uri": ...})` defined CRS

    ```python
    TileMatrixSet(
        ...
        crs="http://www.opengis.net/def/crs/EPSG/0/3857"
    )

    TileMatrixSet(
        ...
        crs={"uri": "http://www.opengis.net/def/crs/EPSG/0/3857"}
    )

    wkt = pyproj.CRS.from_epsg(3857).to_wkt()
    TileMatrixSet(
        ...
        crs={"wkt": wkt}
    )
    ```

* update `TileMatrixSet` representation to use CRS's URI
* remove default for `TileMatrixSet.pointOfOrigin` attribute (**required**)
* add `topLeft` default for `TileMatrixSet.cornerOfOrigin` attribute
* renamed `morecantile.models.CRSType` -> `morecantile.models.CRS`

## 5.1.0 (2024-01-08)

* Simplify bounds calculation by using `TileMatrix.cellSize` instead of `TileMatrix.scaleDenominator`
* remove `TileMatrixSet._resolution` private method

## 5.0.2 (2023-12-01)

* Remove *alias* tiles in `.parent()`, `.children()`, `.neighbors()` and `.tiles()` methods for Variable Matrix Width TileMatrixSets (https://github.com/developmentseed/morecantile/pull/136)

## 5.0.1 (2023-12-01) [DELETED]

* ~~Remove *alias* tiles in `.parent()`, `.children()`, `.neighbors()` and `.tiles()` methods for Variable Matrix Width TileMatrixSets (https://github.com/developmentseed/morecantile/pull/136)~~

## 5.0.0 (2023-07-24)

* update pydantic requirement to `~=2.0`

* add support for TileMatrixSets with Variable Matrix Width

* add `variableMatrixWidths` to the `TileMatrix` model

* add `TileMatrixSet._lr()` (and `lr()`) to retrieve the lower right coordinates of a tile (instead of using upper-left of tile+1)

* switch to `functools.cached_property` to cache properties (instead of cachetools.LRUcache)

* rename `_is_quadtree` property to `is_quadtree` in `TileMatrixSet` model

* fix possible bug in `TileMatrixSet._tile()` (and `.tile()`) method to make sure x or y are not greater than `matrixWidth - 1` or `matrixHeight - 1`

## 4.3.0 (2023-07-11)

* add `.srs` property to `CRSType`
* forward arguments to `pyproj.CRS` methods for `to_epsg()`, `to_wkt()`, `to_proj4()` and `to_json()` CRSType methods

## 4.2.1 (2023-07-02)

* limit pydantic requirement to `~=1.0``

## 4.2.0 (2023-06-09)

* add `to_proj4` and `to_dict` and `to_json` methods to `CRSType`
* remove `TileMatrixSet._crs` (replaced with `TileMatrixSet.crs._pyproj_crs`)

## 4.1.1 (2023-06-07)

* add `to_epsg()` and `to_wkt()` methods to `CRSType` to allow compatibility with `4.0`

```python
import morecantile

tms = morecantile.tms.get("WebMercatorQuad")

tms.crs
>> CRSType(__root__='http://www.opengis.net/def/crs/EPSG/0/3857')

tms.crs.to_epsg()
>> 3857

tms._crs
>> <Projected CRS: EPSG:3857>

tms._crs.to_epsg()
>> 3857
```

## 4.1.0 (2023-06-06)

* Change CRS attribute in model to align more with the TMS spec and fix some OpenAPI schema issues (It should be a string URI or WKT, not a pyproj.CRS)
* add `TileMatrixSet._crs` PrivateAttr to host the `pyproj.CRS` version of the crs
* update `grid_crs` properties in `TileMatrixSet.feature()` result to return the `TileMatrixSet.CRS` (uri/wkt) instead of EPSG code

## 4.0.2 (2023-05-31)

* Fix TileMatrixSet BoundingBox definition (https://github.com/developmentseed/morecantile/pull/122)

## 4.0.1 (2023-05-31)

* Raise a `ValueError` when `nan` bounds are passed to `tiles` (author @samn, https://github.com/developmentseed/morecantile/pull/120)

## 4.0.0 (2023-05-22)

* no change since `4.0.0a1`

## 4.0.0a1 (2023-05-17)

* Fix possible bug when a TileMatrixSet does not have `id`

## 4.0.0a0 (2023-05-15)

* Remove assumption tile rows/cols are ordered in `TileMatrixSet.tiles()` method (author @fsvenson, https://github.com/developmentseed/morecantile/pull/104)
* switch to **TMS 2.0** specification (author @dchirst, https://github.com/developmentseed/morecantile/pull/101). See https://developmentseed.org/morecantile/tms-v2/ for more info.
* remove `NZTM2000` TileMatrixSet (ref: https://github.com/developmentseed/morecantile/issues/103)
* add `rasterio_geographic_crs` to export TMS's geographic CRS to Rasterio's CRS object (author @AndrewAnnex, https://github.com/developmentseed/morecantile/pull/109)
* add `geographic_crs` property in the TileMatrixSet model to return the private `_geographic_crs` attribute
* add cache LRU layer on top of `TileMatrixSet.bbox` method
* changed the input type in `morecantile.defaults.TileMatrixSets.register()` from `Sequence[TileMatrixSet]` to `Dict[str, TileMatrixSets]`

    ```python
    my_custom_tms = ...

    # before
    defaults = morecantile.tms.register([my_custom_tms])

    # now
    defaults = morecantile.tms.register({"MyCustomGrid": my_custom_tms})
    ```

* made `id` and `title` optional in `morecantile.TileMatrixSet.custom()` method

    ```python
    crs = CRS.from_epsg(3031)
    extent = [-948.75, -543592.47, 5817.41, -3333128.95]  # From https:///epsg.io/3031

    # before
    tms = morecantile.TileMatrixSet.custom(extent, crs)
    print(tms.id, tms.title)
    >>> "Custom", "Custom TileMatrixSet"

    # now
    tms = morecantile.TileMatrixSet.custom(extent, crs)
    print(tms.id, tms.title)
    >>> None, None
    ```

* remove `boundingBox` in TileMatrixSet definition when created with `morecantile.TileMatrixSet.custom`

## 3.4.0 (2023-05-15)

* [backported from 4.0] Remove assumption tile rows/cols are ordered in `TileMatrixSet.tiles()` method (author @fsvenson, https://github.com/developmentseed/morecantile/pull/104)
* [backported from 4.0] add `rasterio_geographic_crs` to export TMS's geographic CRS to Rasterio's CRS object (author @AndrewAnnex, https://github.com/developmentseed/morecantile/pull/109)
* [backported from 4.0] add `geographic_crs` property in the TileMatrixSet model to return the private `_geographic_crs` attribute
* [backported from 4.0] add cache LRU layer on top of `TileMatrixSet.bbox` method

## 3.3.0 (2023-03-09)

* sort default TMS (author @jlaura, https://github.com/developmentseed/morecantile/pull/98)
* Switch to ruff for linting and fixing linting issues

## 3.2.5 (2022-12-16)

* Do not parse TMS json files automatically but wait for the TMS to be used

## 3.2.4 (2022-12-14)

* fix `CanadianNAD83_LCC`, `WorldMercatorWGS84Quad` and `EuropeanETRS89_LAEAQuad` TMS
* add `title` option in `morecantile custom` CLI

## 3.2.3 (2022-12-13)

* fix `utils.meters_per_unit` for non earth bodies (author @AndrewAnnex, https://github.com/developmentseed/morecantile/pull/92)
* fix `CRS_to_uri` function to adds ability to export non-EPSG CRSs URIs (author @AndrewAnnex, https://github.com/developmentseed/morecantile/pull/93)

## 3.2.2 (2022-11-25)

* add `morecantile.defaults.TileMatrixSets` in export

## 3.2.1 (2022-10-25)

* add python 3.11 support

## 3.2.0 (2022-10-20)

* add python 3.10 support
* remove python 3.7 support
* switch to pyproject.toml

## 3.1.2 (2022-03-21)

* add support for `foot` and `US survey foot` CRS (https://github.com/developmentseed/morecantile/pull/86)

## 3.1.1 (2022-02-25)

* fix issue with `zoom_for_res` when resolution is smaller than minzoom (author @samn, https://github.com/developmentseed/morecantile/pull/84)

## 3.1.0 (2022-02-18)

* add `parent`, `children`, `neighbors`, `minmax`, `is_valid` methods (https://github.com/developmentseed/morecantile/pull/82)

**breaking changes**

* update `WebMercatorQuad` TMS to match `mercantile` and `GDAL` definition of the half-earth value

## 3.0.5 (2022-02-16)

* truncate geographic Lon/Lat inputs to the TMS geographic bbox instead of `-180., -90., 180., 90.` (https://github.com/developmentseed/morecantile/pull/79)
* remove `utils.truncate_lnglat` function (https://github.com/developmentseed/morecantile/pull/79)

## 3.0.4 (2022-02-16)

* Allow zoom_for_res to work for a TMS with a minzoom > 0 (author @samn, https://github.com/developmentseed/morecantile/pull/78)

## 3.0.3 (2021-12-06)

* add `WGS1984Quad` (`WGS84/epgs:4326`) TileMatrixSet (https://github.com/developmentseed/morecantile/pull/74)

## 3.0.2 (2021-11-12)

* add `_geographic_crs` definition in `__init__` to make sure it's initialized from user input (author @davenquinn, https://github.com/developmentseed/morecantile/pull/72)

## 3.0.1 (2021-11-10)

* rename `_to_wgs84` and `_from_wgs84` private attributes to `_to_geographic` and `_from_geographic` (https://github.com/developmentseed/morecantile/pull/68)
* add `_geographic_crs` private attribute to `morecantile.TileMatrixSet` to define the CRS used in  `_to_geographic` and `_from_geographic` (https://github.com/developmentseed/morecantile/pull/68)
* fix `TileMatrixSet._invert_axis` method to only check axis information (https://github.com/developmentseed/morecantile/pull/71)

## 3.0.0 (2021-09-23)

* no change since 3.0.0a1

## 3.0.0a1 (2021-09-17)

* only import rasterio if needed (https://github.com/developmentseed/morecantile/pull/66)

## 3.0.0a0 (2021-09-09)

* add `.rasterio_crs` properties to TMS for compatibility with rasterio (https://github.com/developmentseed/morecantile/pull/58)
* Use new Class-like notation for namedtuple (https://github.com/developmentseed/morecantile/pull/58)

**breaking changes**

* switch from rasterio to PyProj for CRS definition and projection transformation (https://github.com/developmentseed/morecantile/pull/58)
* remove python 3.6 supports (because of pyproj)

## 2.1.4 (2021-08-20)

* add **NZTM2000Quad** tile matrix set from LINZ (author @blacha, https://github.com/developmentseed/morecantile/pull/57)
* add **quadkey** supports (@author adrian-knauer, https://github.com/developmentseed/morecantile/pull/56)

    ```python
    import morecantile

    tms = morecantile.tms.get("WebMercatorQuad")

    # Tile to Quadkey
    tms.quadkey(486, 332, 10)
    >>> "0313102310"

    # Quadkey to Tile
    tms.quadkey_to_tile("0313102310")
    >>> Tile(486, 332, 10)
    ```

* update `NZTM2000*` CRS uri from `https://www.opengis.net/def/crs/EPSG/0/2193` to `urn:ogc:def:crs:EPSG:2193` (https://github.com/developmentseed/morecantile/pull/61)

## 2.1.3 - Doesn't exists

## 2.1.2 (2021-05-18)

* fix wrong TMS boundingBox definition when using inverted CRS (https://github.com/developmentseed/morecantile/pull/53)

## 2.1.1 (2021-05-17)

* remove `mercantile` dependency.
* raise `PointOutsideTMSBounds` warning when user is doing operations outside TMS bounds.
* fix wrong `xy_bbox` when `tms.boundingBox` use a specific CRS.

## 2.1.0 (2020-12-17)

* add `zoom_level_strategy` option for `TileMatrixSet.zoom_for_res` to match GDAL 3.2.
By default, it is set to `auto`, meaning that it will select the closest zoom level. User can set the strategy to `lower` or `upper` to select below or above zoom levels.
```python
import morecantile
tms = morecantile.tms.get("WebMercatorQuad")

# native resolution of zoom 7 is 1222.9924 m
# native resolution of zoom 8 is 611.4962 m
assert tms.zoom_for_res(612.0) == 8
assert tms.zoom_for_res(612.0, zoom_level_strategy="lower") == 7
assert tms.zoom_for_res(612.0, zoom_level_strategy="upper") == 8
```

## 2.0.1 (2020-11-05)

* simplify `morecantile.TileMatrixSet` default representation

```python
from morecantile import tms

tms.get("WorldCRS84Quad")
>>> <TileMatrixSet title='CRS84 for the World' identifier='WorldCRS84Quad'>

print(tms.get("WorldCRS84Quad").json())
>>> {
    'type': 'TileMatrixSetType',
    'title': 'CRS84 for the World',
    'abstract': None,
    'keywords': None,
    'identifier': 'WorldCRS84Quad',
    'supportedCRS': CRS.from_epsg(4326),
    'wellKnownScaleSet': AnyHttpUrl(...),
    'boundingBox': {
        'type': 'BoundingBoxType',
        'crs': CRS.from_epsg(4326),
        'lowerCorner': (-180.0, -90.0),
        'upperCorner': (180.0, 90.0)},
        'tileMatrix': [...]
    }
```

## 2.0.0 (2020-11-04)

* switch from `CoordBBox` to `rasterio.coords.BoundingBox` (ref: https://github.com/developmentseed/morecantile/issues/38).
* update `morecantile.commons` Tile and Coords to match rasterio's BoundingBox.
* rename `morecantile.models.BoundingBox` to `morecantile.models.TMSBoundingBox` to avoind name colision with rasterio's BoundingBox.
* improve default TMS immutability by making `morecantile.tms.register` to return a new TileMatrixSets instance (ref: https://github.com/developmentseed/morecantile/issues/37)

```python
import morecantile import TileMatrixSet, tms
from rasterio.crs import CRS

crs = CRS.from_epsg(3031)
extent = [-948.75, -543592.47, 5817.41, -3333128.95]  # From https:///epsg.io/3031
custom_tms = TileMatrixSet.custom(extent, crs, identifier="MyCustomTmsEPSG3031")

print(len(tms.list()))
>>> 10

defaults = tms.register(custom_tms)
print(len(tms.list()))
>>> 10

print(len(defaults.list()))
>>> 11
```

## 1.3.1 (2020-10-07)

* remove `pkg_resources` (https://github.com/pypa/setuptools/issues/510, https://github.com/developmentseed/morecantile/pull/36)
* add `TILEMATRIXSET_DIRECTORY` to allow morecantile to load user's TMS

```python
# Save custom TMS to a file
import morecantile
from rasterio.crs import CRS

crs = CRS.from_epsg(3031)
extent = [-948.75, -543592.47, 5817.41, -3333128.95]  # From https:///epsg.io/3031
tms = morecantile.TileMatrixSet.custom(extent, crs, identifier="MyCustomTmsEPSG3031")

with open("/tmp/mytms/MyCustomTmsEPSG3031.json", "w") as f:
    f.write(tms.json(exclude_none=True))
```

```python
import os
os.environ["TILEMATRIXSET_DIRECTORY"] = "/tmp/mytms"

from morecantile import tms
assert "MyCustomTmsEPSG3031" in tms.list()
```

## 1.3.0.post1 (2020-09-30)

* fix TileMatrixSet's model schema bug where pydantic wasn't able to translate `Union[rasterio.crs.CRS, pydantic.AnyHttpUrl]` to a valid schema (ref: https://github.com/developmentseed/morecantile/issues/34)

## 1.3.0 (2020-09-30)

* Allow Custom CRS for custom TMS definition (https://github.com/developmentseed/morecantile/issues/23)
* Extend TMS beyond TMS Document max zoom level (https://github.com/developmentseed/morecantile/pull/28)
* Require rasterio >= 1.1.7 (sept 2020) to support inverted lat/lon TMS (ref: https://github.com/developmentseed/morecantile/issues/26)
* Remove deprecated function
* Add `tms.xy_bbox` and `tms.bbox` properties to return TileMatrixSet boundaries.
* Add `tms.intersect_tms` to check if a bbox intersect with the TileMatrixSet boundaries.
* Avoid out-range tiles (e.g. negative indexes)
* Add `tms.zoom_for_res` function to get the TMS zoom level for a specific resolution (https://github.com/developmentseed/morecantile/issues/31).

## 1.2.0 (2020-06-01)

* add TileMatrixSet minzoom/maxzoom properties
* fix TileMatrixSet.tile calculation
* add TileMatrixSet.tiles function (replicat from mercantile)
* add buffer and projected options to TileMatrixSet.feature method
* removes mercantile as dependencies
* add CLI
* renamed `morecantile.TileMatrixSet.point_towgs84` to `morecantile.TileMatrixSet.lnglat` (matches mercantile)
* renamed `morecantile.TileMatrixSet.point_fromwgs84` to `morecantile.TileMatrixSet.xy` (matches mercantile)
* add `truncate` option in `morecantile.TileMatrixSet.tile` (matches mercantile)
* re-order buffer and precision options in `morecantile.TileMatrixSet.feature` (matches mercantile)
* uses mercantile's tests

## 1.1.1 (2020-05-15)

* Fix bad default TMS files (https://github.com/developmentseed/morecantile/issues/13)
* Add regex in model for identifier validation

## 1.1.0 (2020-05-13)

* better submodule definition
* add `morecantile.tms` object to access and register defaults TileMatrixSet
* Add depreciation warning for `morecantile.TileMatrixSet.load` method

## 1.0.0 (2020-05-11)

Major refactor of Morecantile, which is now based on OGC TileMatrixSet JSON documents.

* use pydantic model to validate TMS JSON documents (https://github.com/developmentseed/morecantile/pull/6, author @geospatial-jeff)
* morecantile methods are part of the TMS model (https://github.com/developmentseed/morecantile/pull/7)

## 0.1.0 (2020-02-03)

* Rename defaults grids (https://github.com/developmentseed/morecantile/issues/1)

## 0.0.1 (2020-01-23)

* Initial release
