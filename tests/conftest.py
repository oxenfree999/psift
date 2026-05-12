import polars as pl
import pytest

from psift.core.loaders import load_csv, load_polars
from psift.core.source import Source


@pytest.fixture(autouse=True)
def clean_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.delenv("FORCE_COLOR", raising=False)
    monkeypatch.delenv("CLICOLOR", raising=False)
    monkeypatch.delenv("CLICOLOR_FORCE", raising=False)
    monkeypatch.delenv("TERM", raising=False)
    monkeypatch.delenv("PSIFT_LOG", raising=False)
    monkeypatch.setenv("COLUMNS", "80")
    # Prevent Rich from reducing width by 1 on Windows legacy consoles.
    # Rich's own test suite does the equivalent via legacy_windows=False.
    monkeypatch.setattr("rich.console.WINDOWS", False)


@pytest.fixture
def tiny_source() -> Source:
    return load_csv("tests/fixtures/tiny.csv")


@pytest.fixture
def large_source() -> Source:
    return load_polars(
        pl.DataFrame(
            {
                "id": range(10_000),
                "value": range(10_000),
            }
        ),
        name="large",
    )
