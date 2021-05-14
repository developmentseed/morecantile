"""Morecantile command line interface"""

import json
import logging
import sys

import click
from rasterio.crs import CRS
from rasterio.rio.helpers import coords

import morecantile

logger = logging.getLogger(__name__)


def configure_logging(verbosity):
    """Configure log verbosity.

    Original code from https://github.com/mapbox/mercantile/blob/71bb3dbdaeb4ccf0e14bfabf1f58d36465cd5289/mercantile/scripts/__init__.py#L13-L26
    License: BSD-3 Original work Copyright 2021 Mapbox
    """
    log_level = max(10, 30 - 10 * verbosity)
    logging.basicConfig(stream=sys.stderr, level=log_level)


def normalize_input(input):
    """Normalize file or string input.

    Original code from https://github.com/mapbox/mercantile/blob/71bb3dbdaeb4ccf0e14bfabf1f58d36465cd5289/mercantile/scripts/__init__.py#L34-L40
    License: BSD-3 Original work Copyright 2021 Mapbox
    """
    try:
        src = click.open_file(input).readlines()
    except IOError:
        src = [input]
    return src


def iter_lines(lines):
    """Iterate over lines of input, stripping and skipping.

    Original code from https://github.com/mapbox/mercantile/blob/71bb3dbdaeb4ccf0e14bfabf1f58d36465cd5289/mercantile/scripts/__init__.py#L43-L48
    License: BSD-3 Original work Copyright 2021 Mapbox
    """
    for line in lines:
        line = line.strip()
        if line:
            yield line


def normalize_source(input):
    """Yield features from GeoJSON source."""
    src = iter(normalize_input(input))
    first_line = next(src)

    # If input is RS-delimited JSON sequence.
    if first_line.startswith(u"\x1e"):

        def feature_gen():
            buffer = first_line.strip(u"\x1e")
            for line in src:
                if line.startswith(u"\x1e"):
                    if buffer:
                        yield json.loads(buffer)
                    buffer = line.strip(u"\x1e")
                else:
                    buffer += line
            else:
                yield json.loads(buffer)

    else:

        def feature_gen():
            yield json.loads(first_line)
            for line in src:
                yield json.loads(line)

    return feature_gen()


# The CLI command group.
@click.group(help="Command line interface for the Morecantile Python package.")
@click.option("--verbose", "-v", count=True, help="Increase verbosity.")
@click.option("--quiet", "-q", count=True, help="Decrease verbosity.")
@click.version_option(version=morecantile.__version__, message="%(version)s")
@click.pass_context
def cli(ctx, verbose, quiet):
    """Execute the main morecantile command"""
    verbosity = verbose - quiet
    configure_logging(verbosity)
    ctx.obj = {}
    ctx.obj["verbosity"] = verbosity


################################################################################
# The shapes command.
@cli.command(short_help="Print the shapes of tiles as GeoJSON.")
# This input is either a filename, stdin, or a string.
@click.argument("input", default="-", required=False)
@click.option(
    "--identifier",
    type=click.Choice(morecantile.tms.list()),
    default="WebMercatorQuad",
    help="TileMatrixSet identifier.",
)
# Coordinate precision option.
@click.option(
    "--precision", type=int, default=None, help="Decimal precision of coordinates."
)
# JSON formatting options.
@click.option(
    "--indent", default=None, type=int, help="Indentation level for JSON output"
)
@click.option(
    "--compact/--no-compact", default=False, help="Use compact separators (',', ':')."
)
@click.option(
    "--projected/--geographic",
    "projected",
    default=False,
    help="Output coordinate system",
)
@click.option(
    "--seq",
    is_flag=True,
    default=False,
    help="Write a RS-delimited JSON sequence (default is LF).",
)
# GeoJSON feature (default) or collection switch. Meaningful only
# when --x-json-seq is used.
@click.option(
    "--feature",
    "output_mode",
    flag_value="feature",
    default=True,
    help="Output as sequence of GeoJSON features (the default).",
)
@click.option(
    "--bbox",
    "output_mode",
    flag_value="bbox",
    help="Output as sequence of GeoJSON bbox arrays.",
)
@click.option(
    "--collect",
    is_flag=True,
    default=False,
    help="Output as a GeoJSON feature collections.",
)
# Optionally write out bboxen in a form that goes
# straight into GDAL utilities like gdalwarp.
@click.option(
    "--extents/--no-extents",
    default=False,
    help="Write shape extents as ws-separated strings (default is " "False).",
)
# Optionally buffer the shapes by shifting the x and y values of each
# vertex by a constant number of decimal degrees or meters (depending
# on whether --geographic or --mercator is in effect).
@click.option(
    "--buffer",
    type=float,
    default=None,
    help="Shift shape x and y values by a constant number",
)
@click.pass_context
def shapes(
    ctx,
    input,
    identifier,
    precision,
    indent,
    compact,
    projected,
    seq,
    output_mode,
    collect,
    extents,
    buffer,
):
    """
    Reads one or more Web Mercator tile descriptions
    from stdin and writes either a GeoJSON feature collection (the
    default) or a JSON sequence of GeoJSON features/collections to
    stdout.

    Input may be a compact newline-delimited sequences of JSON or
    a pretty-printed ASCII RS-delimited sequence of JSON (like
    https://tools.ietf.org/html/rfc8142 and
    https://tools.ietf.org/html/rfc7159).

    Tile descriptions may be either an [x, y, z] array or a JSON
    object of the form {"tile": [x, y, z], "properties": {"name": "foo", ...}}

    In the latter case, the properties object will be used to update
    the properties object of the output feature.

    """
    tms = morecantile.tms.get(identifier)

    dump_kwds = {"sort_keys": True}
    if indent:
        dump_kwds["indent"] = indent
    if compact:
        dump_kwds["separators"] = (",", ":")

    src = normalize_input(input)
    features = []
    col_xs = []
    col_ys = []

    for i, line in enumerate(iter_lines(src)):
        obj = json.loads(line)
        if isinstance(obj, dict):
            x, y, z = obj["tile"][:3]
            props = obj.get("properties")
            fid = obj.get("id")
        elif isinstance(obj, list):
            x, y, z = obj[:3]
            props = {}
            fid = None
        else:
            raise click.BadParameter("{0}".format(obj), param=input, param_hint="input")

        feature = tms.feature(
            (x, y, z),
            fid=fid,
            props=props,
            projected=projected,
            buffer=buffer,
            precision=precision,
        )
        bbox = feature["bbox"]
        w, s, e, n = bbox
        col_xs.extend([w, e])
        col_ys.extend([s, n])

        if collect:
            features.append(feature)
        elif extents:
            click.echo(" ".join(map(str, bbox)))
        else:
            if seq:
                click.echo(u"\x1e")
            if output_mode == "bbox":
                click.echo(json.dumps(bbox, **dump_kwds))
            elif output_mode == "feature":
                click.echo(json.dumps(feature, **dump_kwds))

    if collect and features:
        bbox = [min(col_xs), min(col_ys), max(col_xs), max(col_ys)]
        click.echo(
            json.dumps(
                {"type": "FeatureCollection", "bbox": bbox, "features": features},
                **dump_kwds
            )
        )


################################################################################
# The tiles command.
@cli.command(
    short_help=(
        "Print tiles that overlap or contain a lng/lat point, "
        "bounding box, or GeoJSON objects."
    )
)
# Mandatory Mercator zoom level argument.
@click.argument("zoom", type=int, default=-1)
# This input is either a filename, stdin, or a string.
# Has to follow the zoom arg.
@click.argument("input", default="-", required=False)
@click.option(
    "--identifier",
    type=click.Choice(morecantile.tms.list()),
    default="WebMercatorQuad",
    help="TileMatrixSet identifier.",
)
@click.option(
    "--seq/--lf",
    default=False,
    help="Write a RS-delimited JSON sequence (default is LF).",
)
@click.pass_context
def tiles(ctx, zoom, input, identifier, seq):
    """
    Lists TMS tiles at ZOOM level intersecting
    GeoJSON [west, south, east, north] bounding boxen, features, or
    collections read from stdin. Output is a JSON
    [x, y, z] array.

    Input may be a compact newline-delimited sequences of JSON or
    a pretty-printed ASCII RS-delimited sequence of JSON (like
    https://tools.ietf.org/html/rfc8142 and
    https://tools.ietf.org/html/rfc7159).

    Example:
    $ echo "[-105.05, 39.95, -105, 40]" | morecantiles tiles 12
    Output:
    [852, 1550, 12]
    [852, 1551, 12]
    [853, 1550, 12]
    [853, 1551, 12]

    """
    tms = morecantile.tms.get(identifier)

    for obj in normalize_source(input):
        if isinstance(obj, list):
            bbox = obj
            if len(bbox) == 2:
                bbox += bbox

            if len(bbox) != 4:
                raise click.BadParameter(
                    "{0}".format(bbox), param=input, param_hint="input"
                )

        elif isinstance(obj, dict):
            if "bbox" in obj:
                bbox = obj["bbox"]
            else:
                box_xs = []
                box_ys = []
                for feat in obj.get("features", [obj]):
                    lngs, lats = zip(*list(coords(feat)))
                    box_xs.extend([min(lngs), max(lngs)])
                    box_ys.extend([min(lats), max(lats)])

                bbox = min(box_xs), min(box_ys), max(box_xs), max(box_ys)

        west, south, east, north = bbox
        epsilon = 1.0e-10

        if east != west and north != south:
            # 2D bbox
            # shrink the bounds a small amount so that
            # shapes/tiles round trip.
            west += epsilon
            south += epsilon
            east -= epsilon
            north -= epsilon

        for tile in tms.tiles(west, south, east, north, [zoom], truncate=False):
            vals = (tile.x, tile.y, zoom)
            output = json.dumps(vals)
            if seq:
                click.echo(u"\x1e")

            click.echo(output)


################################################################################
# The tms command.
@cli.command(short_help="Print TileMatrixSet JSON document.")
@click.option(
    "--identifier",
    type=click.Choice(morecantile.tms.list()),
    help="TileMatrixSet identifier.",
    required=True,
)
def tms(identifier):
    """Print TMS JSON."""
    tms = morecantile.tms.get(identifier)
    click.echo(tms.json(exclude_none=True))


################################################################################
# The custom command.
@cli.command(short_help="Create Custom TileMatrixSet")
@click.option(
    "--epsg", type=int, help="EPSG number.", required=True,
)
@click.option(
    "--extent",
    type=float,
    nargs=4,
    help="left, bottom, right, top Bounding box of the Tile Matrix Set.",
    required=True,
)
@click.option(
    "--name",
    type=str,
    help="Identifier of the custom TMS.",
    default="CustomTileMatrixSet",
)
@click.option("--minzoom", type=int, default=0, help="Minumum Zoom level.")
@click.option("--maxzoom", type=int, default=24, help="Maximum Zoom level.")
@click.option("--tile-width", type=int, default=256, help="Width of each tile.")
@click.option("--tile-height", type=int, default=256, help="Height of each tile.")
@click.option(
    "--extent-epsg", type=int, help="EPSG number for the bounding box.",
)
def custom(epsg, extent, name, minzoom, maxzoom, tile_width, tile_height, extent_epsg):
    """Create Custom TMS."""
    extent_crs = CRS.from_epsg(extent_epsg) if extent_epsg else None

    tms = morecantile.TileMatrixSet.custom(
        extent,
        CRS.from_epsg(epsg),
        identifier=name,
        minzoom=minzoom,
        maxzoom=maxzoom,
        tile_width=tile_width,
        tile_height=tile_height,
        extent_crs=extent_crs,
    )
    click.echo(tms.json(exclude_none=True))


################################################################################
# The tms_to_geojson command.
@cli.command(short_help="Print TileMatrixSet MatrixSet as GeoJSON.")
@click.argument("input", type=click.File(mode="r"), default="-", required=False)
@click.option("--level", type=int, required=True, help="Zoom/Matrix level.")
# Coordinate precision option.
@click.option(
    "--precision", type=int, default=None, help="Decimal precision of coordinates."
)
# JSON formatting options.
@click.option(
    "--indent", default=None, type=int, help="Indentation level for JSON output"
)
@click.option(
    "--compact/--no-compact", default=False, help="Use compact separators (',', ':')."
)
@click.option(
    "--projected/--geographic",
    "projected",
    default=False,
    help="Output coordinate system",
)
@click.option(
    "--seq",
    is_flag=True,
    default=False,
    help="Write a RS-delimited JSON sequence (default is LF).",
)
# GeoJSON feature (default) or collection switch. Meaningful only
# when --x-json-seq is used.
@click.option(
    "--feature",
    "output_mode",
    flag_value="feature",
    default=True,
    help="Output as sequence of GeoJSON features (the default).",
)
@click.option(
    "--bbox",
    "output_mode",
    flag_value="bbox",
    help="Output as sequence of GeoJSON bbox arrays.",
)
@click.option(
    "--collect",
    is_flag=True,
    default=False,
    help="Output as a GeoJSON feature collections.",
)
# Optionally write out bboxen in a form that goes
# straight into GDAL utilities like gdalwarp.
@click.option(
    "--extents/--no-extents",
    default=False,
    help="Write shape extents as ws-separated strings (default is " "False).",
)
# Optionally buffer the shapes by shifting the x and y values of each
# vertex by a constant number of decimal degrees or meters (depending
# on whether --geographic or --mercator is in effect).
@click.option(
    "--buffer",
    type=float,
    default=None,
    help="Shift shape x and y values by a constant number",
)
def tms_to_geojson(
    input,
    level,
    precision,
    indent,
    compact,
    projected,
    seq,
    output_mode,
    collect,
    extents,
    buffer,
):
    """Print TMS document as GeoJSON."""
    tms = morecantile.TileMatrixSet(**json.load(input))
    matrix = tms.matrix(level)

    dump_kwds = {"sort_keys": True}
    if indent:
        dump_kwds["indent"] = indent
    if compact:
        dump_kwds["separators"] = (",", ":")

    features = []
    col_xs = []
    col_ys = []

    for x in range(0, matrix.matrixWidth):
        for y in range(0, matrix.matrixHeight):
            feature = tms.feature(
                (x, y, level), projected=projected, buffer=buffer, precision=precision,
            )
            bbox = feature["bbox"]
            w, s, e, n = bbox
            col_xs.extend([w, e])
            col_ys.extend([s, n])

            if collect:
                features.append(feature)
            elif extents:
                click.echo(" ".join(map(str, bbox)))
            else:
                if seq:
                    click.echo(u"\x1e")
                if output_mode == "bbox":
                    click.echo(json.dumps(bbox, **dump_kwds))
                elif output_mode == "feature":
                    click.echo(json.dumps(feature, **dump_kwds))

    if collect and features:
        bbox = [min(col_xs), min(col_ys), max(col_xs), max(col_ys)]
        feature_collection = {
            "type": "FeatureCollection",
            "bbox": bbox,
            "features": features,
        }
        click.echo(json.dumps(feature_collection, **dump_kwds))
