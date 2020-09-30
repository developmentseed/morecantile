### List supported grids

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

### Load a default grid
```python
import morecantile

tms = morecantile.tms.get("WebMercatorQuad")
```

### Iterate through matrices
```python
for matrix in tms:
    assert isinstance(matrix, morecantile.models.TileMatrix)
```

### Define custom grid

```python
import morecantile
from rasterio.crs import CRS

crs = CRS.from_epsg(3031)
extent = [-948.75, -543592.47, 5817.41, -3333128.95]  # From https:///epsg.io/3031
tms = morecantile.TileMatrixSet.custom(extent, crs, identifier="MyCustomTmsEPSG3031")

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

!!! important
    starting with `morecantile==1.3.0`, you can create TMS using custom CRS.

```python
import morecantile
from rasterio.crs import CRS

crs = CRS.from_proj4("+proj=stere +lat_0=90 +lon_0=0 +k=2 +x_0=0 +y_0=0 +R=3396190 +units=m +no_defs")
extent = [-13584760.000,-13585240.000,13585240.000,13584760.000]
tms = morecantile.TileMatrixSet.custom(extent, crs, identifier="MarsNPolek2MOLA5k")
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
