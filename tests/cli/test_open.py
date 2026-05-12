"""CLI tests for `psift open <source>`."""

from pathlib import Path

import pytest
from typer.testing import CliRunner

from psift.cli.main import cli
from psift.cli.state import ExitCode
from psift.tui.app import PsiftApp

runner = CliRunner()


def test_open_loads_source_and_runs_app(monkeypatch: pytest.MonkeyPatch) -> None:
    invocations: list[str] = []

    def fake_run(self: PsiftApp, *_args: object, **_kwargs: object) -> None:
        invocations.append(self.source.name)

    monkeypatch.setattr(PsiftApp, "run", fake_run)
    result = runner.invoke(cli, ["open", "tests/fixtures/tiny.csv"])
    assert result.exit_code == 0
    assert invocations == ["tiny"]


def test_open_missing_file_exits_with_error(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(PsiftApp, "run", lambda *_args, **_kwargs: None)
    missing = tmp_path / "does_not_exist.csv"
    result = runner.invoke(cli, ["open", str(missing)])
    combined = (result.output or "") + (getattr(result, "stderr", "") or "")
    assert result.exit_code == ExitCode.ERROR
    assert "not found" in combined.lower()


def test_open_unsupported_extension_exits_with_error(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(PsiftApp, "run", lambda *_args, **_kwargs: None)
    bad = tmp_path / "data.xyz"
    bad.touch()
    result = runner.invoke(cli, ["open", str(bad)])
    combined = (result.output or "") + (getattr(result, "stderr", "") or "")
    assert result.exit_code == ExitCode.ERROR
    assert "unsupported" in combined.lower()
