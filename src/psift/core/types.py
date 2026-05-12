"""Shared core enums."""

from enum import StrEnum


class DType(StrEnum):
    """Broad dtype categories used by source metadata."""

    numeric = "numeric"
    string = "string"
    boolean = "boolean"
    date = "date"
    datetime = "datetime"
    time = "time"
    duration = "duration"
    categorical = "categorical"
    binary = "binary"
    list_ = "list"
    struct = "struct"
    null = "null"
    unknown = "unknown"


class SourceKind(StrEnum):
    """How a source was opened."""

    csv = "csv"
    tsv = "tsv"
    parquet = "parquet"
    arrow = "arrow"
    polars = "polars"
    memory = "memory"
