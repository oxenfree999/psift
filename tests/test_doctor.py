"""Tests for psift doctor command."""

import json
from importlib.metadata import PackageNotFoundError

import pytest
from typer.testing import CliRunner

from psift.cli.doctor import _runtime_versions, _terminal_capabilities, format_text, get_system_info
from psift.cli.main import cli

runner = CliRunner()


def test_runtime_versions_present() -> None:
    versions = _runtime_versions()
    assert versions["typer"] is True


def test_runtime_versions_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    def raise_not_found(name: str) -> str:
        raise PackageNotFoundError(name)

    monkeypatch.setattr("psift.cli.doctor.version", raise_not_found)
    assert _runtime_versions() == {"typer": False}


@pytest.mark.parametrize(
    ("env_value", "expected"),
    [
        ("truecolor", True),
        ("24bit", True),
        ("TRUECOLOR", True),
        (None, False),
        ("", False),
        ("256color", False),
    ],
)
def test_terminal_capabilities(monkeypatch: pytest.MonkeyPatch, env_value: str | None, expected: bool) -> None:
    if env_value is None:
        monkeypatch.delenv("COLORTERM", raising=False)
    else:
        monkeypatch.setenv("COLORTERM", env_value)
    assert _terminal_capabilities() == {"truecolor": expected}


def test_get_system_info_keys() -> None:
    info = get_system_info()
    assert set(info.keys()) == {"psift", "python", "platform", "runtime", "terminal"}


def test_format_text_includes_section_labels() -> None:
    info = get_system_info()
    output = format_text(info)
    for label in ("psift", "python", "platform", "runtime:", "terminal:"):
        assert label in output


def test_doctor_text_contains_expected_labels() -> None:
    result = runner.invoke(cli, ["doctor"])
    assert result.exit_code == 0
    for label in ("psift", "python", "platform", "runtime:", "terminal:", "typer", "truecolor"):
        assert label in result.output


def test_doctor_json_is_valid_dict() -> None:
    result = runner.invoke(cli, ["doctor", "--json"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert isinstance(data, dict)
    assert set(data.keys()) == {"psift", "python", "platform", "runtime", "terminal"}
