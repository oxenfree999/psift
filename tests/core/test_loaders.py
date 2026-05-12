"""Tests for source loaders."""

from pathlib import Path

import polars as pl
import pytest

from psift.core.loaders import (
    load_arrow_ipc,
    load_parquet,
    load_polars,
    load_records,
    load_tsv,
    open_source,
)
from psift.core.source import Source
from psift.core.types import DType, SourceKind


def test_load_csv_returns_source(tiny_source: Source) -> None:
    assert tiny_source.name == "tiny"
    assert tiny_source.kind is SourceKind.csv
    assert tiny_source.row_count_estimate is None
    assert tiny_source.column_names() == ("id", "item", "quantity", "price", "active", "date")
    assert tiny_source.column_names() == tuple(tiny_source.lf.collect_schema().names())
    assert tiny_source.columns[0].category is DType.numeric
    assert tiny_source.columns[1].category is DType.string


def test_load_tsv_returns_tsv_source(tmp_path: Path) -> None:
    source_path = tmp_path / "tiny.tsv"
    source_path.write_text("id\titem\n1\tnotebook\n", encoding="utf-8")

    source = load_tsv(source_path)

    assert source.kind is SourceKind.tsv
    assert source.column_names() == ("id", "item")


def test_open_source_dispatches_csv(tiny_source: Source) -> None:
    source = open_source(tiny_source.origin)
    assert source.kind is SourceKind.csv
    assert source.column_names() == tiny_source.column_names()


def test_load_parquet_returns_source(tmp_path: Path) -> None:
    source_path = tmp_path / "items.parquet"
    pl.DataFrame({"id": [1], "item": ["notebook"]}).write_parquet(source_path)

    source = load_parquet(source_path)

    assert source.kind is SourceKind.parquet
    assert source.column_names() == ("id", "item")


def test_load_arrow_ipc_returns_source(tmp_path: Path) -> None:
    source_path = tmp_path / "items.arrow"
    pl.DataFrame({"id": [1], "item": ["notebook"]}).write_ipc(source_path)

    source = load_arrow_ipc(source_path)

    assert source.kind is SourceKind.arrow
    assert source.column_names() == ("id", "item")


def test_load_polars_sets_row_count_for_eager_frame() -> None:
    source = load_polars(pl.DataFrame({"id": [1, 2]}), name="items")
    assert source.kind is SourceKind.polars
    assert source.row_count_estimate == 2


def test_load_records_sets_memory_kind() -> None:
    source = load_records([{"id": 1, "item": "notebook"}])
    assert source.kind is SourceKind.memory
    assert source.row_count_estimate == 1


def test_open_source_rejects_unsupported_suffix(tmp_path: Path) -> None:
    source_path = tmp_path / "items.json"
    source_path.write_text("[]", encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported source file type"):
        open_source(source_path)


def test_file_loader_reports_missing_kind(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="tsv file not found"):
        load_tsv(tmp_path / "missing.tsv")
