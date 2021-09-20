
## 3.0.0 (2021-09-20)

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
