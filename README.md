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

**Morecantile** follows the **OGC Two Dimensional Tile Matrix Set** specification found in [http://docs.opengeospatial.org/is/17-083r2/17-083r2.html](http://docs.opengeospatial.org/is/17-083r2/17-083r2.html)

**Note**: Variable matrix width tile set are not supported.

## Install

```bash
$ python -m pip install -U pip
$ python -m pip install morecantile

# Or install from source:

$ python -m pip install -U pip
$ python -m pip install git+https://github.com/developmentseed/morecantile.git
```

### Defaults Grids

- **CanadianNAD83_LCC**: Lambert conformal conic NAD83 for Canada - EPSG:3978
- **EuropeanETRS89_LAEAQuad**: ETRS89-extended / LAEA Europe - EPGS:3035
- **LINZAntarticaMapTilegrid**: LINZ Antarctic Map Tile Grid (Ross Sea Region) - EPSG:5482
- **NZTM2000**: LINZ NZTM2000 Map Tile Grid - EPSG:2193
- **NZTM2000Quad**: LINZ NZTM2000 Map Tile Grid - EPSG:2193
- **UPSAntarcticWGS84Quad**: Universal Polar Stereographic WGS 84 Quad for Antarctic - EPSG:5042
- **UPSArcticWGS84Quad**: Universal Polar Stereographic WGS 84 Quad for Arctic - EPSG:5041
- **UTM31WGS84Quad**: Example of UTM grid - EPSG:32631
- **WebMercatorQuad**: Spherical Mercator - EPGS:3857 (default grid for Web Mercator based maps)
- **WGS1984Quad**: EPSG:4326 for the World - EPGS:4326 (WGS84)
- **WorldCRS84Quad**: CRS84 for the World
- **WorldMercatorWGS84Quad**: Elliptical Mercator projection - EPGS:3395

ref: http://schemas.opengis.net/tms/1.0/json/examples/

## Implementations

- [rio-tiler](https://github.com/cogeotiff/rio-tiler): Create tile from raster using Morecantile TMS.
- [timvt](https://github.com/developmentseed/timvt): A lightweight PostGIS based dynamic vector tile server.
- [planetcantile](https://github.com/AndrewAnnex/planetcantile): Tile matrix sets for other planets.

## Changes

See [CHANGES.md](https://github.com/developmentseed/morecantile/blob/main/CHANGES.md).

## Contribution & Development

See [CONTRIBUTING.md](https://github.com/developmentseed/morecantile/blob/main/CONTRIBUTING.md)

## License

See [LICENSE](https://github.com/developmentseed/morecantile/blob/main/LICENSE)

## Authors

Created by [Development Seed](<http://developmentseed.org>)
