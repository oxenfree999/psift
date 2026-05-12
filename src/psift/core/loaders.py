"""Lazy source loaders."""

from collections.abc import Callable
from pathlib import Path
from typing import Any

import polars as pl

from psift.core.source import ColumnSpec, Source, dtype_category
from psift.core.types import SourceKind


def _source_from_lazy(
    lf: pl.LazyFrame,
    *,
    name: str,
    kind: SourceKind,
    origin: str,
    row_count_estimate: int | None = None,
) -> Source:
    columns = tuple(
        ColumnSpec(name=column_name, polars_dtype=dtype, category=dtype_category(dtype))
        for column_name, dtype in lf.collect_schema().items()
    )
    return Source(
        name=name,
        kind=kind,
        origin=origin,
        _lf=lf,
        columns=columns,
        row_count_estimate=row_count_estimate,
    )


def _load_data(
    path: str | Path,
    *,
    kind: SourceKind,
    scan: Callable[[Path], pl.LazyFrame],
    name: str | None = None,
) -> Source:
    source_path = Path(path).expanduser()
    if not source_path.exists():
        msg = f"{kind.value} file not found: {source_path}"
        raise FileNotFoundError(msg)
    lf = scan(source_path)
    return _source_from_lazy(lf, name=name or source_path.stem, kind=kind, origin=str(source_path))


def load_csv(path: str | Path, *, separator: str = ",", name: str | None = None) -> Source:
    """Load a delimited text file as a lazy source."""
    kind = SourceKind.tsv if separator == "\t" else SourceKind.csv
    return _load_data(
        path,
        kind=kind,
        scan=lambda source_path: pl.scan_csv(
            source_path,
            separator=separator,
            infer_schema_length=10_000,
            try_parse_dates=True,
        ),
        name=name,
    )


def load_tsv(path: str | Path, *, name: str | None = None) -> Source:
    """Load a TSV file as a lazy source."""
    return load_csv(path, separator="\t", name=name)


def load_parquet(path: str | Path, *, name: str | None = None) -> Source:
    """Load a Parquet file as a lazy source."""
    return _load_data(path, kind=SourceKind.parquet, scan=pl.scan_parquet, name=name)


def load_arrow_ipc(path: str | Path, *, name: str | None = None) -> Source:
    """Load an Arrow IPC or Feather file as a lazy source."""
    return _load_data(path, kind=SourceKind.arrow, scan=pl.scan_ipc, name=name)


def load_polars(frame: pl.DataFrame | pl.LazyFrame, *, name: str = "df") -> Source:
    """Wrap an in-memory Polars frame as a source."""
    lf = frame.lazy() if isinstance(frame, pl.DataFrame) else frame
    row_count = frame.height if isinstance(frame, pl.DataFrame) else None
    return _source_from_lazy(
        lf,
        name=name,
        kind=SourceKind.polars,
        origin="<memory>",
        row_count_estimate=row_count,
    )


def load_records(rows: list[dict[str, Any]], *, name: str = "records") -> Source:
    """Wrap in-memory records as a source."""
    return _source_from_lazy(
        pl.DataFrame(rows).lazy(),
        name=name,
        kind=SourceKind.memory,
        origin="<memory>",
        row_count_estimate=len(rows),
    )


_OPENERS = {
    ".csv": load_csv,
    ".tsv": load_tsv,
    ".parquet": load_parquet,
    ".pq": load_parquet,
    ".arrow": load_arrow_ipc,
    ".ipc": load_arrow_ipc,
    ".feather": load_arrow_ipc,
}


def open_source(path: str | Path, *, name: str | None = None) -> Source:
    """Open a supported filesystem source by suffix."""
    source_path = Path(path).expanduser()
    opener = _OPENERS.get(source_path.suffix.lower())
    if opener is None:
        msg = f"Unsupported source file type: {source_path}"
        raise ValueError(msg)
    return opener(source_path, name=name)
