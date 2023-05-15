# TMS v2.0 and Morecantile v4

In September 2022, the Open Geospatial Consortium released an updated specification for [Tile Matrix Sets - version 2.0](https://docs.ogc.org/is/17-083r4/17-083r4.html).

This updated spec includes some breaking changes that alter the TMS JSON document. Some of these changes include:

- [Addition of a `uri` parameter for TileMatrixSets registered on the official OGC NA TileMatrixSets registry](https://docs.ogc.org/is/17-083r4/21-066r1.html#_identifying_with_uri_a_well_known_tilematrixset_in_an_authoritative_registry)
- [`identifier` renamed to `id`](https://docs.ogc.org/is/17-083r4/21-066r1.html#_json_encoding_rules_to_derive_a_more_natural_json_encoding_from_uml) in both TileMatrix and TileMatrixSet
- [Only `crs` and `tileMatrices` are required in `TileMatrixSet`](https://github.com/opengeospatial/2D-Tile-Matrix-Set/blob/master/schemas/tms/2.0/json/tileMatrixSet.json#L6)
- [`supportedCRS` renamed to `crs`](https://docs.ogc.org/is/17-083r4/21-066r1.html#_renaming_supportedcrs_to_crs)
- [`tileMatrix` renamed to `tileMatrices`](https://docs.ogc.org/is/17-083r4/21-066r1.html#_json_encoding_rules_to_derive_a_more_natural_json_encoding_from_uml)
- [`topLeftCorner` renamed to `pointOfOrigin`](https://docs.ogc.org/is/17-083r4/21-066r1.html#_replacing_topleftcorner_by_pointoforigin)
- [Add `cellSize` and `cornerOfOrigin` (Optional) parameters to TileMatrix](https://docs.ogc.org/is/17-083r4/21-066r1.html#_adding_cellsize_and_corneroforigin)
- [Remove `type` object properties](https://docs.ogc.org/is/17-083r4/21-066r1.html#_removing_type_object_properties)
- [Added optional axis ordering](https://docs.ogc.org/is/17-083r4/21-066r1.html#_adding_optional_orderedaxes_to_highlight_crs_axis_ordering
)

Morecantile version 4 has been updated to support the updated TMS 2.0 specification. When using the predefined Tile Matrix Sets or making a custom TMS this should work as normal with some renamed properties (specified above).

If you want to create a new Tile Matrix Set from a JSON made to the old TMS v1 specification, there is a new class method called `from_v1` that does this.

```python
from morecantile.models import TileMatrixSet
import json

with open("tms_v1.json") as f:
    data = json.load(f)


TileMatrixSet.from_v1(data)
```

