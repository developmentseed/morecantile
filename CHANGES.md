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
