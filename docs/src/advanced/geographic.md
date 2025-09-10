
Several methods/properties of the **morecantile.TileMatrixSet** object use Geographic Coordinates Reference System (CRS) to transform coordinates from/to the TMS's CRS:

- `TileMatrixSet.lnglat(x, y)`: Transform point(x,y) to geographic longitude and latitude
- `TileMatrixSet.xy(lng, lat)`: Transform geographic longitude and latitude coordinates to TMS CRS
- `TileMatrixSet.ul(Tile)`: Return the upper left coordinates of the tile in geographic coordinate reference system
- `TileMatrixSet.lr(Tile)`: Return the lower right coordinates of the tile in geographic coordinate reference system
- `TileMatrixSet.bounds(Tile)`: Return the bounding box of the tile in geographic coordinate reference system
- `TileMatrixSet.bbox`: Return TMS bounding box in geographic coordinate reference system

For those methods/properties, the Geographic CRS is defined by the TileMatrixSet CRS's geographic CRS (`CRS.geodetic_crs`). The most common one is the `World Geodetic System 1984` (`WGS84` or `EPSG:4326`) but it's not the one used by default.

```python
import morecantile 

morecantile.tms.get("WebMercatorQuad").geographic_crs
>> <Geographic 2D CRS: EPSG:4326>
Name: WGS 84
Axis Info [ellipsoidal]:
- Lat[north]: Geodetic latitude (degree)
- Lon[east]: Geodetic longitude (degree)
Area of Use:
- name: World.
- bounds: (-180.0, -90.0, 180.0, 90.0)
Datum: World Geodetic System 1984 ensemble
- Ellipsoid: WGS 84
- Prime Meridian: Greenwich

morecantile.tms.get("CanadianNAD83_LCC").geographic_crs
>> <Geographic 2D CRS: EPSG:4269>
Name: NAD83
Axis Info [ellipsoidal]:
- Lat[north]: Geodetic latitude (degree)
- Lon[east]: Geodetic longitude (degree)
Area of Use:
- name: North America - onshore and offshore: Canada - Alberta; British Columbia; Manitoba; New Brunswick; Newfoundland and Labrador; Northwest Territories; Nova Scotia; Nunavut; Ontario; Prince Edward Island; Quebec; Saskatchewan; Yukon. Puerto Rico. United States (USA) - Alabama; Alaska; Arizona; Arkansas; California; Colorado; Connecticut; Delaware; Florida; Georgia; Hawaii; Idaho; Illinois; Indiana; Iowa; Kansas; Kentucky; Louisiana; Maine; Maryland; Massachusetts; Michigan; Minnesota; Mississippi; Missouri; Montana; Nebraska; Nevada; New Hampshire; New Jersey; New Mexico; New York; North Carolina; North Dakota; Ohio; Oklahoma; Oregon; Pennsylvania; Rhode Island; South Carolina; South Dakota; Tennessee; Texas; Utah; Vermont; Virginia; Washington; West Virginia; Wisconsin; Wyoming. US Virgin Islands. British Virgin Islands.
- bounds: (167.65, 14.92, -40.73, 86.45)
Datum: North American Datum 1983
- Ellipsoid: GRS 1980
- Prime Meridian: Greenwich
```

### Overwriting the Geographic CRS

There are **two** mechanisms to overwrite the TMS's geographic CRS.

- `TileMatrixSet.set_geographic_crs(crs)`: Overwrite the TMS's Geographic CRS (`TileMatrixSet._geographic_crs` private attribute)

```python
import morecantile
import pyproj

tms = morecantile.tms.get("CanadianNAD83_LCC")
tms.geographic_crs
>> <Geographic 2D CRS: EPSG:4269>
...

tms.set_geographic_crs(pyproj.CRS.from_epsg(4326))
tms.geographic_crs
>> <Geographic 2D CRS: EPSG:4326>
...
```

- `MORECANTILE_DEFAULT_GEOGRAPHIC_CRS` environment variable

```python
import os
os.environ["MORECANTILE_DEFAULT_GEOGRAPHIC_CRS"] = "EPSG:4326"

import morecantile

tms = morecantile.tms.get("CanadianNAD83_LCC")
tms.geographic_crs
>> <Geographic 2D CRS: EPSG:4326>
```

Some methods have `geographic_crs` option to specify the CRS to use to transf the default CRS:

- `TileMatrixSet.tile(lng, lat, *, geographic_crs=None)`: Get the tile for a given geographic longitude and latitude pair
- `TileMatrixSet.tiles(west, south, east, north, *, geographic_crs=None)`: Get the tiles overlapped by a geographic bounding box
