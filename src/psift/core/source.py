"""Source metadata for tabular data."""

from collections.abc import Mapping
from dataclasses import dataclass, field

import polars as pl

from psift.core.types import DType, SourceKind

_DTYPE_CATEGORIES = {
    "Int8": DType.numeric,
    "Int16": DType.numeric,
    "Int32": DType.numeric,
    "Int64": DType.numeric,
    "UInt8": DType.numeric,
    "UInt16": DType.numeric,
    "UInt32": DType.numeric,
    "UInt64": DType.numeric,
    "Float32": DType.numeric,
    "Float64": DType.numeric,
    "Decimal": DType.numeric,
    "String": DType.string,
    "Boolean": DType.boolean,
    "Date": DType.date,
    "Datetime": DType.datetime,
    "Time": DType.time,
    "Duration": DType.duration,
    "Categorical": DType.categorical,
    "Enum": DType.categorical,
    "Binary": DType.binary,
    "List": DType.list_,
    "Array": DType.list_,
    "Struct": DType.struct,
    "Null": DType.null,
}


@dataclass(frozen=True, slots=True)
class ColumnSpec:
    """A single column schema entry."""

    name: str
    polars_dtype: pl.DataType
    category: DType


@dataclass(frozen=True, slots=True)
class Source:
    """A named, typed handle onto a Polars lazy frame."""

    name: str
    kind: SourceKind
    origin: str
    _lf: pl.LazyFrame = field(repr=False)
    columns: tuple[ColumnSpec, ...] = field(default_factory=tuple)
    row_count_estimate: int | None = None

    @property
    def lf(self) -> pl.LazyFrame:
        """Return the base lazy frame."""
        return self._lf

    def column_names(self) -> tuple[str, ...]:
        """Return column names in source order."""
        return tuple(column.name for column in self.columns)

    def schema_dict(self) -> Mapping[str, pl.DataType]:
        """Return a name-to-dtype schema mapping."""
        return {column.name: column.polars_dtype for column in self.columns}


def dtype_category(dtype: pl.DataType) -> DType:
    """Bucket a Polars dtype into a broad psift category."""
    return _DTYPE_CATEGORIES.get(str(dtype.base_type()), DType.unknown)
