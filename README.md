# Morecantile

Construct and use map tile grids (a.k.a TileMatrixSet / TMS).

[![Packaging status](https://badge.fury.io/py/morecantile.svg)](https://badge.fury.io/py/morecantile)
[![CircleCI](https://circleci.com/gh/developmentseed/morecantile.svg?style=svg)](https://circleci.com/gh/cogeotiff/morecantile)
[![codecov](https://codecov.io/gh/developmentseed/morecantile/branch/master/graph/badge.svg)](https://codecov.io/gh/cogeotiff/morecantile)

The name is an homage to [mercantile](https://github.com/mapbox/mercantile), a great tools to work with Web Mercator tile indexes. This module aims to mimic `mercatile` features but for other grids.

This module follows the **OGC Two Dimensional Tile Matrix Set** specification found in [http://docs.opengeospatial.org/is/17-083r2/17-083r2.html](http://docs.opengeospatial.org/is/17-083r2/17-083r2.html)

Note: Variable matrix width tile set are not supported.

## Install

```bash
$ pip install -U pip
$ pip install morecantile

# Or install from source:

$ pip install git+https://github.com/developmentseed/morecantile.git
```

## How To

```
    +-------------+-------------+  ymax
    |             |             |
    |    x: 0     |    x: 1     |
    |    y: 0     |    y: 0     |
    |    z: 1     |    z: 1     |
    |             |             |
    +-------------+-------------+ 
    |             |             |
    |    x: 0     |    x: 1     |
    |    y: 1     |    y: 1     |
    |    z: 1     |    z: 1     |
    |             |             |
    +-------------+-------------+  ymin

xmin                            xmax
```

### Defaults Grids

- **CanadianNAD83_LCC**: Lambert conformal conic NAD83 for Canada - EPSG:3978
- **EuropeanETRS89_LAEAQuad**: ETRS89-extended / LAEA Europe - EPGS:3035
- **LINZAntarticaMapTilegrid**: LINZ Antarctic Map Tile Grid (Ross Sea Region) - EPSG:5482
- **NZTM2000**: LINZ NZTM2000 Map Tile Grid - EPSG:2193
- **UPSAntarcticWGS84Quad**: Universal Polar Stereographic WGS 84 Quad for Antarctic - EPSG:5042
- **UPSArcticWGS84Quad**: Universal Polar Stereographic WGS 84 Quad for Arctic - EPSG:5041
- **UTM31WGS84Quad**: Example of UTM grid - EPSG:32631
- **WebMercatorQuad**: Spherical Mercator - EPGS:3857 (default grid for Web Mercator based maps)
- **WorldCRS84Quad**: CRS84 for the World - EPGS:4326 (WGS84)
- **WorldMercatorWGS84Quad**: Elliptical Mercator projection - EPGS:3395

ref: http://schemas.opengis.net/tms/1.0/json/examples/

```python
import morecantile

print(morecantile.tms.list())
>> [
    'LINZAntarticaMapTilegrid',
    'EuropeanETRS89_LAEAQuad',
    'CanadianNAD83_LCC',
    'UPSArcticWGS84Quad',
    'NZTM2000',
    'UTM31WGS84Quad',
    'UPSAntarcticWGS84Quad',
    'WorldMercatorWGS84Quad',
    'WorldCRS84Quad',
    'WebMercatorQuad'
]
```

### Load default grid
```python
import morecantile

tms = morecantile.tms.get("WebMercatorQuad")
```

### Define custom grid
```python
import morecantile
from rasterio.crs import CRS

crs = CRS.from_epsg(3031)
extent = [-948.75, -543592.47, 5817.41, -3333128.95]  # From https:///epsg.io/3031
tms = morecantile.TileMatrixSet.custom(extent, crs, indentifier="MyCustomTmsEPSG3031")

print(tms.matrix(0).dict(exclude_none=True))
{
    "type": "TileMatrixType",
    "identifier": "0",
    "scaleDenominator": 38916524.55357144,
    "topLeftCorner": [-948.75, -3333128.95],
    "tileWidth": 256,
    "tileHeight": 256,
    "matrixWidth": 1,
    "matrixHeight": 1
}
```

And register the TMS
```python
morecantile.tms.register(tms)
tms = morecantile.tms.get("MyCustomTmsEPSG3031")
assert "MyCustomTmsEPSG3031" in morecantile.tms.list()
```

### Create tile and get bounds
```python
import morecantile

tms = morecantile.tms.get("WebMercatorQuad")

# Get the bounds for tile Z=4, X=10, Y=10 in the input projection
tms.xy_bounds(morecantile.Tile(10, 10, 4))
>> CoordsBbox(xmin=5009377.085697308, ymin=-7514065.628545959, xmax=7514065.628545959, ymax=-5009377.085697308)

# Get the bounds for tile Z=4, X=10, Y=10 in LatLon (WGS84)
tms.bounds(morecantile.Tile(10, 10, 4))  
>> CoordsBbox(xmin=44.999999999999964, ymin=-55.776573018667634, xmax=67.4999999999999, ymax=-40.97989806962009)
```

### Find tile for lat/lon
```python
import morecantile

tms = morecantile.tms.get("WebMercatorQuad")

tms.tile(159.31, -42, 4) 
>> Tile(x=15, y=10, z=4)

# Or using coordinates in input CRS
x, y = ts.point_fromwgs84(159.31, -42)
ts._tile(x, y, 4)
>> Tile(x=11, y=10, z=4)
```

### Get Geojson Feature

```python
import morecantile

tms = morecantile.tms.get("WebMercatorQuad")

tms.feature(morecantile.Tile(10, 10, 4))

>> {
    'type': 'Feature',
    'bbox': [
        44.999999999999964,
        -55.776573018667634,
        67.4999999999999,
        -40.97989806962009
    ],
    'id': 'Tile(x=10, y=10, z=4)',
    'geometry': {
        'type': 'Polygon',
        'coordinates': [[
            [44.999999999999964, -55.776573018667634],
            [44.999999999999964, -40.97989806962009],
            [67.4999999999999, -40.97989806962009],
            [67.4999999999999, -55.776573018667634],
            [44.999999999999964, -55.776573018667634]
        ]]
    },
    'properties': {
        'title': 'XYZ tile Tile(x=10, y=10, z=4)',
        'grid_name': 'WebMercatorQuad',
        'grid_crs': 'EPSG:3857'
    }
}
```

## Morecantile + Pydantic

Morecantile uses [Pydantic](https://pydantic-docs.helpmanual.io) to define and validate TileMatrixSet documents.

From Pydantic docs:
> Define how data should be in pure, canonical python; validate it with pydantic.

Pydantic model enforce the TileMatrixSet OGC specification for the whole project by validating each items.

Because we use pydantic model to handle the TileMatrixSets you can uses pydantic's [helper functions](https://pydantic-docs.helpmanual.io/usage/models/#helper-functions) directly. 

```python
import morecantile

my_tms_doc = "~/a_tms_doc.json"

tms = morecantile.TileMatrixSet.parse_file(my_tms_doc)
```

## Contribution & Development

Issues and pull requests are more than welcome.

**dev install**

```bash
$ git clone https://github.com/developmentseed/morecantile.git
$ cd rio-cogeo
$ pip install -e .[dev]
```

**Python >=3.7 only**

This repo is set to use `pre-commit` to run *isort*, *flake8*, *pydocstring*, *black* ("uncompromising Python code formatter") and mypy when committing new code.

```
$ pre-commit install

$ git add .

$ git commit -m'my change'
isort....................................................................Passed
black....................................................................Passed
Flake8...................................................................Passed
Verifying PEP257 Compliance..............................................Passed
mypy.....................................................................Passed

$ git push origin
```

## About
Created by [Development Seed](<http://developmentseed.org>)
