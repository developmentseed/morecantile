# Morecantile

Construct and use map tile grids in different projection.

[![Packaging status](https://badge.fury.io/py/morecantile.svg)](https://badge.fury.io/py/morecantile)
[![CircleCI](https://circleci.com/gh/developmentseed/morecantile.svg?style=svg)](https://circleci.com/gh/cogeotiff/morecantile)
[![codecov](https://codecov.io/gh/developmentseed/morecantile/branch/master/graph/badge.svg)](https://codecov.io/gh/cogeotiff/morecantile)

The name is an homage to [mercantile](https://github.com/mapbox/mercantile), a great tools to work with Web Mercator tile indexes. This module aims to mimic `mercatile` features but for other projections.


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

### Define custom grid
```python
import morecantile
from rasterio.crs import CRS

epsg = 3031
extent = [-948.75, -543592.47, 5817.41, -3333128.95]  # From https:///epsg.io/3031
ts = morecantile.TileSchema(CRS.from_epsg(epsg), extent)

# Or

# epsg:3031 is one of the default grids available in morecantile
# see https://github.com/developmentseed/morecantile/blob/master/__init__.py#L94-L99
crs, args = morecantile.default_grids.get(3031)
ts = morecantile.TileSchema(crs, **args)
```

### Create tile and get bounds
```python
# Get the bounds for tile Z=4, X=10, Y=10 in the input projection
ts.xy_bounds(morecantile.Tile(10, 10, 4))
>> CoordsBbox(xmin=1742511.5500000003, ymin=-5250935.28, xmax=1916857.5800000003, ymax=-5076589.25)

# Get the bounds for tile Z=4, X=10, Y=10 in LatLon (WGS84)
ts.bounds(morecantile.Tile(10, 10, 4))  
>> CoordsBbox(xmin=161.0554963794693, ymin=-41.54639259511877, xmax=159.94535469608172, ymax=-43.27127363762563)
```

### Find tile for lat/lon
```python
ts.tile(159.31, -42, 4) 
>> Tile(x=11, y=10, z=4)

# Or using coordinates in input CRS
x, y = ts.point_fromwgs84(159.31, -42)
ts._tile(x, y, z)
>> Tile(x=11, y=10, z=4)
```

### Get Geojson Feature

```python
ts.feature(morecantile.Tile(10, 10, 4))

>> {
    'type': 'Feature',
    'bbox': [
        159.94535469608172,
        -43.27127363762563,
        161.0554963794693,
        -41.54639259511877
    ],
    'id': 'Tile(x=10, y=10, z=4)',
    'geometry': {
        'type': 'Polygon',
        'coordinates': [[
            [161.0554963794693, -41.54639259511877],
            [161.0554963794693, -43.27127363762563],
            [159.94535469608172, -43.27127363762563],
            [159.94535469608172, -41.54639259511877],
            [161.0554963794693, -41.54639259511877]
        ]]
    },
    'properties': {
        'title': 'XYZ tile Tile(x=10, y=10, z=4)',
        'grid_crs': 'EPSG:3031'
    }
}
```

## Contribution & Development

Issues and pull requests are more than welcome.

**dev install**

```bash
$ git clone https://github.com/developmentseed/morecantile.git
$ cd rio-cogeo
$ pip install -e .[dev]
```

**Python3.7 only**

This repo is set to use `pre-commit` to run *flake8*, *pydocstring* and *black*
("uncompromising Python code formatter") when commiting new code.

```bash
$ pre-commit install
```
