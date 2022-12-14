
# Morecantile CLI

The CLI is heavily inspired from mercantile's CLI.

```
morecantile --help
Usage: morecantile [OPTIONS] COMMAND [ARGS]...

  Command line interface for the Morecantile Python package.

Options:
  -v, --verbose  Increase verbosity.
  -q, --quiet    Decrease verbosity.
  --version      Show the version and exit.
  --help         Show this message and exit.

Commands:
  tiles           Print tiles that overlap or contain a lng/lat point, bounding box, or GeoJSON objects.
  shapes          Print the shapes of tiles as GeoJSON.
  custom          Create Custom TileMatrixSet
  tms             Print TileMatrixSet JSON document.
  tms-to-geojson  Print TileMatrixSet MatrixSet as GeoJSON.
```

## Tiles

With the tiles command you can write descriptions of tiles intersecting with a geographic point, bounding box, or GeoJSON object.

```
$ morecantile tiles --help
Usage: morecantile tiles [OPTIONS] [ZOOM] [INPUT]

  Lists TMS tiles at ZOOM level intersecting GeoJSON [west, south, east,
  north] bounding boxen, features, or collections read from stdin. Output is
  a JSON [x, y, z] array.

  Input may be a compact newline-delimited sequences of JSON or a pretty-
  printed ASCII RS-delimited sequence of JSON (like
  https://tools.ietf.org/html/rfc8142 and
  https://tools.ietf.org/html/rfc7159).

  Example: $ echo "[-105.05, 39.95, -105, 40]" | morecantiles tiles 12
  Output: [852, 1550, 12] [852, 1551, 12] [853, 1550, 12] [853, 1551, 12]

Options:
  --identifier TileMatrixSet identifier.
               One of :
                - LINZAntarticaMapTilegrid
                - EuropeanETRS89_LAEAQuad
                - CanadianNAD83_LCC
                - UPSArcticWGS84Quad
                - NZTM2000
                - NZTM2000Quad
                - UTM31WGS84Quad
                - UPSAntarcticWGS84Quad
                - WorldMercatorWGS84Quad
                - WorldCRS84Quad
                - WGS1984Quad
                - WebMercatorQuad
  --seq / --lf                    Write a RS-delimited JSON sequence (default is LF).
  --help                          Show this message and exit.
```

## Shapes

The shapes command writes TMS tile shapes to several forms of GeoJSON.

```
$ morecantile shapes --help
Usage: morecantile shapes [OPTIONS] [INPUT]

  Reads one or more Web Mercator tile descriptions from stdin and writes
  either a GeoJSON feature collection (the default) or a JSON sequence of
  GeoJSON features/collections to stdout.

  Input may be a compact newline-delimited sequences of JSON or a pretty-
  printed ASCII RS-delimited sequence of JSON (like
  https://tools.ietf.org/html/rfc8142 and
  https://tools.ietf.org/html/rfc7159).

  Tile descriptions may be either an [x, y, z] array or a JSON object of the
  form {"tile": [x, y, z], "properties": {"name": "foo", ...}}

  In the latter case, the properties object will be used to update the
  properties object of the output feature.

Options:
  --identifier TileMatrixSet identifier.
               One of :
                - LINZAntarticaMapTilegrid
                - EuropeanETRS89_LAEAQuad
                - CanadianNAD83_LCC
                - UPSArcticWGS84Quad
                - NZTM2000
                - NZTM2000Quad
                - UTM31WGS84Quad
                - UPSAntarcticWGS84Quad
                - WorldMercatorWGS84Quad
                - WorldCRS84Quad
                - WGS1984Quad
                - WebMercatorQuad
  --precision INTEGER             Decimal precision of coordinates.
  --indent INTEGER                Indentation level for JSON output
  --compact / --no-compact        Use compact separators (',', ':').
  --projected / --geographic      Output coordinate system
  --seq                           Write a RS-delimited JSON sequence (default is LF).
  --feature                       Output as sequence of GeoJSON features (the default).
  --bbox                          Output as sequence of GeoJSON bbox arrays.
  --collect                       Output as a GeoJSON feature collections.
  --extents / --no-extents        Write shape extents as ws-separated strings (default is False).
  --buffer FLOAT                  Shift shape x and y values by a constant number
  --help                          Show this message and exit.
```

## Custom

With the custom command you can create custom TileMatrixSet documents.

```
$ morecantile custom --help
Usage: morecantile custom [OPTIONS]

  Create Custom TMS.

Options:
  --epsg INTEGER         EPSG number.  [required]
  --extent FLOAT...      left, bottom, right, top Bounding box of the Tile Matrix Set.  [required]
  --name TEXT            Identifier of the custom TMS.
  --minzoom INTEGER      Minumum Zoom level.
  --maxzoom INTEGER      Maximum Zoom level.
  --tile-width INTEGER   Width of each tile.
  --tile-height INTEGER  Height of each tile.
  --extent-epsg INTEGER  EPSG number for the bounding box.
  --title TEXT           Tile Matrix Set title.
  --help                 Show this message and exit.
```

## tms

The tms command returns the TileMatrixSet document

```
$ morecantile tms --help
Usage: morecantile tms [OPTIONS]

  Print TMS JSON.

Options:
  --identifier TileMatrixSet identifier.
               One of :
                - LINZAntarticaMapTilegrid
                - EuropeanETRS89_LAEAQuad
                - CanadianNAD83_LCC
                - UPSArcticWGS84Quad
                - NZTM2000
                - NZTM2000Quad
                - UTM31WGS84Quad
                - UPSAntarcticWGS84Quad
                - WorldMercatorWGS84Quad
                - WorldCRS84Quad
                - WGS1984Quad
                - WebMercatorQuad
  --help                          Show this message and exit.
```

## tms-to-geojson

Create a GeoJSON from a TMS document

```
$ morecantile tms-to-geojson --help
Usage: morecantile tms-to-geojson [OPTIONS] [INPUT]

  Print TMS document as GeoJSON.

Options:
  --level INTEGER             Zoom/Matrix level.  [required]
  --precision INTEGER         Decimal precision of coordinates.
  --indent INTEGER            Indentation level for JSON output
  --compact / --no-compact    Use compact separators (',', ':').
  --projected / --geographic  Output coordinate system
  --seq                       Write a RS-delimited JSON sequence (default is LF).
  --feature                   Output as sequence of GeoJSON features (the default).
  --bbox                      Output as sequence of GeoJSON bbox arrays.
  --collect                   Output as a GeoJSON feature collections.
  --extents / --no-extents    Write shape extents as ws-separated strings (default is False).
  --buffer FLOAT              Shift shape x and y values by a constant number
  --help                      Show this message and exit.
```

## Examples

```
$ rio bounds eu.tif | morecantile tiles --zoom 1  # like mercantiles

$ morecantile custom --epsg 3413 --extent -4194300 -4194300 4194300 4194300 --minzoom 0 --maxzoom 8 --tile-width 512 --tile-height 512 | morecantile tms-to-geojson --level 3 --projected --collect > l3.geojson

$ rio bounds eu.tif | morecantile tiles 4 --identifier EuropeanETRS89_LAEAQuad  | morecantile shapes --identifier EuropeanETRS89_LAEAQuad --collect > z4.geojson
```
