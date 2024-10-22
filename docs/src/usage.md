
### Load one TMS grid
```python
import morecantile

tms = morecantile.tms.get("WebMercatorQuad")
tms
>>> <TileMatrixSet title='Google Maps Compatible for the World' id='WebMercatorQuad' crs='http://www.opengis.net/def/crs/EPSG/0/3857>
```

### Create tile and get bounds
```python
import morecantile

tms = morecantile.tms.get("WebMercatorQuad")

# Get the bounds for tile Z=4, X=10, Y=10 in the input projection
tms.xy_bounds(morecantile.Tile(10, 10, 4))
>>> BoundingBox(left=5009377.085697308, bottom=-7514065.628545959, right=7514065.628545959, top=-5009377.085697308)

# Get the bounds for tile Z=4, X=10, Y=10 in LatLon (WGS84)
tms.bounds(morecantile.Tile(10, 10, 4))
>>> BoundingBox(left=44.999999999999964, bottom=-55.776573018667634, right=67.4999999999999, top=-40.97989806962009)
```

### Find tile for lat/lon
```python
import morecantile

tms = morecantile.tms.get("WebMercatorQuad")

tms.tile(159.31, -42, 4)
>>> Tile(x=15, y=10, z=4)

# Or using coordinates in input CRS
x, y = tms.xy(159.31, -42)
print(x, y)
>>> (17734308.078276414, -5160979.444049781)

tms._tile(x, y, 4)
>>> Tile(x=15, y=10, z=4)
```

### Get Geojson Feature

```python
import morecantile

tms = morecantile.tms.get("WebMercatorQuad")

tms.feature(morecantile.Tile(10, 10, 4))

>>> {
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

### Define custom grid

You can create custom TMS grid using `morecantile.TileMatrixSet.custom` method.

Here are the available options:

- **extent** (*list of float, REQUIRED*]: a list of coordinates in form of `[xmin, ymin, xmax, ymax]` describing the extend of the TMS

- **crs** (*pyproj.CRS, REQUIRED*): Coordinate reference system of the grid

- **tile_width** (*int, defaults to `256`*): Width of each tile of this tile matrix in pixels (variable width is not supported)

- **tile_height** (*int, defaults to `256`*): Height of each tile of this tile matrix in pixels (variable height is not supported)

- **matrix_scale** (*list of int, default to `[1, 1]`*): Tiling schema coalescence coefficient (see http://docs.opengeospatial.org/is/17-083r2/17-083r2.html#14)

- **extent_crs** (*pyproj.CRS, defaults to TMS CRS*): `extent`'s coordinate reference system

- **minzoom** (*int, defaults to `0`*): Tile Matrix Set minimum zoom level

- **maxzoom** (*int, defaults to `24`*): Tile Matrix Set maximum zoom level

- **title** (*str, defaults to `Custom TileMatrixSet`*): Tile Matrix Set title

- **id** (*str, defaults to `Custom`*): Tile Matrix Set identifier

- **ordered_axes** (*list of str, Optional*): Override Axis order (e.g `["N", "S"]`) else default to CRS's metadata

- **screen_pixel_size** (*float, optional*): Rendering pixel size. `0.28` mm was the actual pixel size of a common display from 2005 and considered as standard by OGC.

- **decimation_base** (*int, optional*): How tiles are divided at each zoom level (default is 2). Must be greater than 1.


```python
import morecantile
from pyproj import CRS

crs = CRS.from_epsg(3031)
extent = [-948.75, -543592.47, 5817.41, -3333128.95]  # From https:///epsg.io/3031
customEPGS3031 = morecantile.TileMatrixSet.custom(extent, crs, id="MyCustomTmsEPSG3031")

print(customEPGS3031.matrix(0).dict(exclude_none=True))
>>> {
    "type": "TileMatrixType",
    "id": "0",
    "scaleDenominator": 38916524.55357144,
    "pointOfOrigin": [
        -948.75,
        -3333128.95
    ],
    "tileWidth": 256,
    "tileHeight": 256,
    "matrixWidth": 1,
    "matrixHeight": 1
}
```

## Use morecantile TMS store

morecantile provides a `TileMatrixSets` class to *store* Tile Matrix Set definition. This object can easily be extended to include your own custom TMS.

### List supported grids

```python
import morecantile

print(morecantile.tms.list())
>>> [
    'LINZAntarticaMapTilegrid',
    'EuropeanETRS89_LAEAQuad',
    'CanadianNAD83_LCC',
    'UPSArcticWGS84Quad',
    'NZTM2000Quad',
    'UTM31WGS84Quad',
    'UPSAntarcticWGS84Quad',
    'WorldMercatorWGS84Quad',
    'WorldCRS84Quad',
    'WGS1984Quad',
    'WebMercatorQuad'
]
```

### Register a custom TMS

```python
default_tms = morecantile.tms.register({"MyCustomTmsEPSG3031": customEPGS3031})
assert "MyCustomTmsEPSG3031" in default_tms.list()

tms = default_tms.get("MyCustomTmsEPSG3031")
tms
>>> <TileMatrixSet title='None' id='MyCustomTmsEPSG3031' crs='epsg:3031>
```

### Automatically register TMS documents

Since the release of morecantile `1.3.1`, users can automatically extend morecantile's default TMS with their custom TMS JSON files stored in a directory, by setting `TILEMATRIXSET_DIRECTORY` environment.

!!! important
    Morecantile will look for all `.json` files within the directory referenced by `TILEMATRIXSET_DIRECTORY`.

    - filename HAVE TO be the same as the TMS id
    - filename HAVE TO be *without special characters* `[a-zA-Z0-9_]`

## Morecantile + Pydantic

Morecantile uses [Pydantic](https://pydantic-docs.helpmanual.io) to define and validate TileMatrixSet documents.

From Pydantic docs:
> Define how data should be in pure, canonical python; validate it with pydantic.

Pydantic model enforce the TileMatrixSet OGC specification for the whole project by validating each items.

Because we use pydantic model to handle the TileMatrixSets you can uses pydantic's [methods](https://docs.pydantic.dev/2.0/usage/models/#model-methods-and-properties) directly.

```python
import morecantile

my_tms_doc = "~/a_tms_doc.json"

tms = morecantile.TileMatrixSet.parse_file(my_tms_doc)

# print the TMS as json
print(tms.model_dump_json(exclude_none=True))

# print the TMS as dict
print(tms.model_dump(exclude_none=True))
```
