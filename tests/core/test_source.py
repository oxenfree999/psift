"""Tests for source metadata."""

import polars as pl

from psift.core.source import ColumnSpec, Source, dtype_category
from psift.core.types import DType, SourceKind


def test_source_normalizes_columns_to_tuple() -> None:
    source = Source(
        name="sample",
        kind=SourceKind.memory,
        origin="<memory>",
        _lf=pl.DataFrame({"id": [1]}).lazy(),
        columns=(ColumnSpec("id", pl.Int64(), DType.numeric),),
        row_count_estimate=1,
    )

    assert source.column_names() == ("id",)
    assert source.schema_dict() == {"id": pl.Int64()}
    assert isinstance(source.columns, tuple)


def test_dtype_category_maps_common_polars_types() -> None:
    assert dtype_category(pl.Int64()) is DType.numeric
    assert dtype_category(pl.Float64()) is DType.numeric
    assert dtype_category(pl.String()) is DType.string
    assert dtype_category(pl.Boolean()) is DType.boolean
    assert dtype_category(pl.Date()) is DType.date
    assert dtype_category(pl.Datetime("us")) is DType.datetime
    assert dtype_category(pl.List(pl.Int64)) is DType.list_
