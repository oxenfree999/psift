"""Tests for core enums."""

from psift.core.types import DType, SourceKind


def test_dtype_values_cover_phase_one_categories() -> None:
    assert {dtype.value for dtype in DType} == {
        "numeric",
        "string",
        "boolean",
        "date",
        "datetime",
        "time",
        "duration",
        "categorical",
        "binary",
        "list",
        "struct",
        "null",
        "unknown",
    }


def test_source_kind_values_cover_phase_one_sources() -> None:
    assert {kind.value for kind in SourceKind} == {
        "csv",
        "tsv",
        "parquet",
        "arrow",
        "polars",
        "memory",
    }
