# Morecantile

<p align="center">
  <img height="500" src="https://github.com/developmentseed/morecantile/assets/10407788/a1523c6d-e255-4dc6-a201-20029715858a"/>
  <p align="center">Construct and use map tile grids (a.k.a TileMatrixSet / TMS).</p>

</p>
<p align="center">
  <a href="https://github.com/developmentseed/morecantile/actions?query=workflow%3ACI" target="_blank">
      <img src="https://github.com/developmentseed/morecantile/workflows/CI/badge.svg" alt="Test">
  </a>
  <a href="https://codecov.io/gh/developmentseed/morecantile" target="_blank">
      <img src="https://codecov.io/gh/developmentseed/morecantile/branch/main/graph/badge.svg" alt="Coverage">
  </a>
  <a href="https://pypi.org/project/morecantile" target="_blank">
      <img src="https://img.shields.io/pypi/v/morecantile?color=%2334D058&label=pypi%20package" alt="Package version">
  </a>
  <a href="https://pypistats.org/packages/morecantile" target="_blank">
      <img src="https://img.shields.io/pypi/dm/morecantile.svg" alt="Downloads">
  </a>
  <a href="https://github.com/developmentseed/morecantile/blob/main/LICENSE" target="_blank">
      <img src="https://img.shields.io/github/license/developmentseed/morecantile.svg" alt="License">
  </a>
</p>

---

**Documentation**: <a href="https://developmentseed.org/morecantile/" target="_blank">https://developmentseed.org/morecantile/</a>

**Source Code**: <a href="https://github.com/developmentseed/morecantile" target="_blank">https://github.com/developmentseed/morecantile</a>

---

Morecantile is like [mercantile](https://github.com/mapbox/mercantile) (the best tool to work with Web Mercator tile indexes), but with support for other TileMatrixSet grids.

**Morecantile** follows the **OGC Two Dimensional Tile Matrix Set** specification **2.0** found in [https://docs.ogc.org/is/17-083r4/17-083r4.html](https://docs.ogc.org/is/17-083r4/17-083r4.html)

| Morecantile Version | OGC Specification Version | Link
| ------------------- | ------------------------- |---------
| 4.0                 | 2.0                       | https://docs.ogc.org/is/17-083r4/17-083r4.html
| 3.0 and earlier     | 1.0                       | http://docs.opengeospatial.org/is/17-083r2/17-083r2.html

**Note**: Variable matrix width tile set are not supported.

## Install

```bash
$ python -m pip install -U pip
$ python -m pip install morecantile

# Or install from source:
$ python -m pip install -U pip
$ python -m pip install git+https://github.com/developmentseed/morecantile.git
```

## Usage

```python
import morecantile

tms = morecantile.tms.get("WebMercatorQuad")

# Get TMS bounding box
print(tms.xy_bbox)
>>> BoundingBox(
    left=-20037508.342789244,
    bottom=-20037508.34278919,
    right=20037508.34278919,
    top=20037508.342789244,
)

# Get the bounds for tile Z=4, X=10, Y=10 in the TMS's CRS (e.g epsg:3857)
print(tms.xy_bounds(morecantile.Tile(10, 10, 4)))
>>> BoundingBox(
    left=5009377.085697308,
    bottom=-7514065.628545959,
    right=7514065.628545959,
    top=-5009377.085697308,
)

# Get the bounds for tile Z=4, X=10, Y=10 in Geographic CRS (e.g epsg:4326)
print(tms.bounds(morecantile.Tile(10, 10, 4)))
>>> BoundingBox(
    left=44.999999999999964,
    bottom=-55.776573018667634,
    right=67.4999999999999,
    top=-40.97989806962009,
)
```

More info can be found at https://developmentseed.org/morecantile/usage/

### Defaults Grids

`morecantile` provides a set of default TMS grids:

- **CanadianNAD83_LCC**: Lambert conformal conic NAD83 for Canada - EPSG:3978
- **EuropeanETRS89_LAEAQuad**: ETRS89-extended / LAEA Europe - EPGS:3035
- **LINZAntarticaMapTilegrid**: LINZ Antarctic Map Tile Grid (Ross Sea Region) - EPSG:5482
- **NZTM2000Quad**: LINZ NZTM2000 Map Tile Grid - EPSG:2193
- **UPSAntarcticWGS84Quad**: Universal Polar Stereographic WGS 84 Quad for Antarctic - EPSG:5042
- **UPSArcticWGS84Quad**: Universal Polar Stereographic WGS 84 Quad for Arctic - EPSG:5041
- **UTM31WGS84Quad**: Example of UTM grid - EPSG:32631
- **WebMercatorQuad**: Spherical Mercator - EPGS:3857 (default grid for Web Mercator based maps)
- **WGS1984Quad**: EPSG:4326 for the World - EPGS:4326 (WGS84)
- **WorldCRS84Quad**: CRS84 for the World
- **WorldMercatorWGS84Quad**: Elliptical Mercator projection - EPGS:3395

ref: https://schemas.opengis.net/tms/2.0/json/examples/tilematrixset/

## Implementations

- [rio-tiler](https://github.com/cogeotiff/rio-tiler): Create tile from raster using Morecantile TMS.
- [titiler](https://github.com/developmentseed/titiler): A modern dynamic tile server built on top of FastAPI and Rasterio/GDAL.
- [tipg](https://github.com/developmentseed/tipg): OGC Features and Tiles API.
- [planetcantile](https://github.com/AndrewAnnex/planetcantile): Tile matrix sets for other planets.
- [supermorecado](https://github.com/developmentseed/supermorecado): Extend the functionality of morecantile with additional commands.


## Changes

See [CHANGES.md](https://github.com/developmentseed/morecantile/blob/main/CHANGES.md).

## Contribution & Development

See [CONTRIBUTING.md](https://github.com/developmentseed/morecantile/blob/main/CONTRIBUTING.md)

## License

See [LICENSE](https://github.com/developmentseed/morecantile/blob/main/LICENSE)

## Authors

Created by [Development Seed](<http://developmentseed.org>)
