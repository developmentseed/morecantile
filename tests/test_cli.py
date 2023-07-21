"""Tests of the morecantile CLI"""

import pytest
from click.testing import CliRunner

from morecantile.scripts.cli import cli


def test_cli_shapes():
    """
    Test shapes.

    From https://github.com/mapbox/mercantile/blob/master/tests/test_cli.py
    """
    runner = CliRunner()
    result = runner.invoke(cli, ["shapes", "--precision", "6"], "[106, 193, 9]")
    assert result.exit_code == 0
    assert (
        result.output
        == '{"bbox": [-105.46875, 39.909736, -104.765625, 40.446947], "geometry": {"coordinates": [[[-105.46875, 39.909736], [-105.46875, 40.446947], [-104.765625, 40.446947], [-104.765625, 39.909736], [-105.46875, 39.909736]]], "type": "Polygon"}, "id": "(106, 193, 9)", "properties": {"grid_crs": "http://www.opengis.net/def/crs/EPSG/0/3857", "grid_name": "WebMercatorQuad", "title": "XYZ tile (106, 193, 9)"}, "type": "Feature"}\n'
    )

    # tile as arg
    result = runner.invoke(cli, ["shapes", "[106, 193, 9]", "--precision", "6"])
    assert result.exit_code == 0
    assert (
        result.output
        == '{"bbox": [-105.46875, 39.909736, -104.765625, 40.446947], "geometry": {"coordinates": [[[-105.46875, 39.909736], [-105.46875, 40.446947], [-104.765625, 40.446947], [-104.765625, 39.909736], [-105.46875, 39.909736]]], "type": "Polygon"}, "id": "(106, 193, 9)", "properties": {"grid_crs": "http://www.opengis.net/def/crs/EPSG/0/3857", "grid_name": "WebMercatorQuad", "title": "XYZ tile (106, 193, 9)"}, "type": "Feature"}\n'
    )

    # buffer
    result = runner.invoke(
        cli, ["shapes", "[106, 193, 9]", "--buffer", "1.0", "--precision", "6"]
    )
    assert result.exit_code == 0
    assert (
        result.output
        == '{"bbox": [-106.46875, 38.909736, -103.765625, 41.446947], "geometry": {"coordinates": [[[-106.46875, 38.909736], [-106.46875, 41.446947], [-103.765625, 41.446947], [-103.765625, 38.909736], [-106.46875, 38.909736]]], "type": "Polygon"}, "id": "(106, 193, 9)", "properties": {"grid_crs": "http://www.opengis.net/def/crs/EPSG/0/3857", "grid_name": "WebMercatorQuad", "title": "XYZ tile (106, 193, 9)"}, "type": "Feature"}\n'
    )

    # Output is compact
    result = runner.invoke(cli, ["shapes", "--compact"], "[106, 193, 9]")
    assert result.exit_code == 0
    assert '"type":"Feature"' in result.output.strip()

    # Output is indented
    result = runner.invoke(cli, ["shapes", "--indent", "8"], "[106, 193, 9]")
    assert result.exit_code == 0
    assert '        "type": "Feature"' in result.output.strip()

    # Shapes are collected into a feature collection
    result = runner.invoke(cli, ["shapes", "--collect", "--feature"], "[106, 193, 9]")
    assert result.exit_code == 0
    assert "FeatureCollection" in result.output

    # geojson is in WebMercator Projection
    with pytest.warns(UserWarning):
        result = runner.invoke(
            cli,
            ["shapes", "[106, 193, 9]", "--extents", "--projected", "--precision", "3"],
        )
        assert result.exit_code == 0
        assert result.output == "-11740727.545 4852834.052 -11662456.028 4931105.569\n"

    with pytest.warns(UserWarning):
        # JSON text sequences of bboxes are output.
        result = runner.invoke(
            cli,
            [
                "shapes",
                "[106, 193, 9]",
                "--seq",
                "--bbox",
                "--projected",
                "--precision",
                "3",
            ],
        )
        assert result.exit_code == 0
        assert (
            result.output
            == "\x1e\n[-11740727.545, 4852834.052, -11662456.028, 4931105.569]\n"
        )

    # shapes_props_fid
    result = runner.invoke(
        cli,
        [
            "shapes",
            '{"tile": [106, 193, 9], "properties": {"title": "foo"}, "id": "42"}',
        ],
    )
    assert result.exit_code == 0
    assert '"title": "foo"' in result.output
    assert '"id": "42"' in result.output


def test_cli_shapesWGS84():
    """Test shapes with other projection."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["shapes", "--precision", "6", "--identifier", "WorldMercatorWGS84Quad"],
        "[106, 193, 9]",
    )
    assert result.exit_code == 0
    assert (
        result.output
        == '{"bbox": [-105.46875, 40.099155, -104.765625, 40.636956], "geometry": {"coordinates": [[[-105.46875, 40.099155], [-105.46875, 40.636956], [-104.765625, 40.636956], [-104.765625, 40.099155], [-105.46875, 40.099155]]], "type": "Polygon"}, "id": "(106, 193, 9)", "properties": {"grid_crs": "http://www.opengis.net/def/crs/EPSG/0/3395", "grid_name": "WorldMercatorWGS84Quad", "title": "XYZ tile (106, 193, 9)"}, "type": "Feature"}\n'
    )


def test_cli_tiles_ok():
    """Test tile with correct bounds."""
    runner = CliRunner()
    result = runner.invoke(cli, ["tiles", "14"], "[-105, 39.99, -104.99, 40]")
    assert result.exit_code == 0
    assert result.output == "[3413, 6202, 14]\n[3413, 6203, 14]\n"


def test_cli_tiles_bad_bounds():
    """Bounds of len 3 are bad."""
    runner = CliRunner()
    result = runner.invoke(cli, ["tiles", "14"], "[-105, 39.99, -104.99]")
    assert result.exit_code == 2


def test_cli_tiles_multi_bounds():
    """A LF-delimited sequence can be used as input."""
    runner = CliRunner()
    result = runner.invoke(
        cli, ["tiles", "14"], "[-105, 39.99, -104.99, 40]\n[-105, 39.99, -104.99, 40]"
    )
    assert result.exit_code == 0
    assert len(result.output.strip().split("\n")) == 4


def test_cli_tiles_multi_bounds_seq():
    """A JSON text sequence can be used as input."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["tiles", "14"],
        "\x1e\n[-105, 39.99, -104.99, 40]\n\x1e\n[-105, 39.99, -104.99, 40]",
    )
    assert result.exit_code == 0
    assert len(result.output.strip().split("\n")) == 4


def test_cli_tiles_implicit_stdin():
    """stdin."""
    runner = CliRunner()
    result = runner.invoke(cli, ["tiles", "14"], "[-105, 39.99, -104.99, 40]")
    assert result.exit_code == 0
    assert result.output == "[3413, 6202, 14]\n[3413, 6203, 14]\n"


def test_cli_tiles_arg():
    """tiles arg."""
    runner = CliRunner()
    result = runner.invoke(cli, ["tiles", "14", "[-105, 39.99, -104.99, 40]"])
    assert result.exit_code == 0
    assert result.output == "[3413, 6202, 14]\n[3413, 6203, 14]\n"


def test_cli_tiles_geosjon():
    """Geojson input."""
    collection = '{"features": [{"geometry": {"coordinates": [[[-105.46875, 39.909736], [-105.46875, 40.446947], [-104.765625, 40.446947], [-104.765625, 39.909736], [-105.46875, 39.909736]]], "type": "Polygon"}, "id": "(106, 193, 9)", "properties": {"title": "XYZ tile (106, 193, 9)"}, "type": "Feature"}], "type": "FeatureCollection"}'
    runner = CliRunner()
    result = runner.invoke(cli, ["tiles", "9"], collection)
    assert result.exit_code == 0
    assert result.output == "[106, 193, 9]\n[106, 194, 9]\n"


def test_cli_strict_overlap_contain():
    """Input from shapes."""
    runner = CliRunner()
    result1 = runner.invoke(cli, ["shapes"], "[2331,1185,12]")
    assert result1.exit_code == 0
    result2 = runner.invoke(cli, ["tiles", "12"], result1.output)
    assert result2.exit_code == 0
    assert result2.output == "[2331, 1185, 12]\n"


def test_cli_tiles_seq():
    """return a sequence of tiles."""
    runner = CliRunner()
    result = runner.invoke(cli, ["tiles", "14", "--seq"], "[14.0859, 5.798]")
    assert result.exit_code == 0
    assert result.output == "\x1e\n[8833, 7927, 14]\n"


def test_cli_tiles_points():
    """Create tile from a point."""
    runner = CliRunner()
    result = runner.invoke(cli, ["tiles", "14"], "[14.0859, 5.798]")
    assert result.exit_code == 0
    assert result.output == "[8833, 7927, 14]\n"

    result = runner.invoke(
        cli, ["tiles", "14"], '{"type":"geometry","coordinates":[14.0859, 5.798]}'
    )
    assert result.exit_code == 0
    assert result.output == "[8833, 7927, 14]\n"
