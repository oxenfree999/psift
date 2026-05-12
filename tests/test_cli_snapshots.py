"""Snapshot tests for CLI help and version output.

These tests lock the exact text of every help screen and the version
string.  When the CLI surface changes intentionally, run:

    just snap

to accept the new output.
"""

import pytest
import typer
from inline_snapshot import snapshot
from typer.testing import CliRunner

from psift.cli.main import cli

runner = CliRunner()


def test_main_help() -> None:
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert typer.unstyle(result.output) == snapshot("""\
                                                                                \n\
 Usage: psift [OPTIONS] COMMAND [ARGS]...                                       \n\
                                                                                \n\
 A terminal tabular data explorer.                                              \n\
                                                                                \n\
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --version             -V        Show version.                                │
│ --install-completion            Install completion for the current shell.    │
│ --show-completion               Show completion for the current shell, to    │
│                                 copy it or customize the installation.       │
│ --help                -h        Show this message and exit.                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ doctor   Check psift environment and report status.                          │
│ open     Open a file in psift.                                               │
│ version  Show psift version.                                                 │
╰──────────────────────────────────────────────────────────────────────────────╯

""")


def test_doctor_help() -> None:
    result = runner.invoke(cli, ["doctor", "--help"])
    assert result.exit_code == 0
    assert typer.unstyle(result.output) == snapshot("""\
                                                                                \n\
 Usage: psift doctor [OPTIONS]                                                  \n\
                                                                                \n\
 Check psift environment and report status.                                     \n\
                                                                                \n\
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --json            Output JSON instead of text.                               │
│ --help  -h        Show this message and exit.                                │
╰──────────────────────────────────────────────────────────────────────────────╯

""")


def test_open_help() -> None:
    result = runner.invoke(cli, ["open", "--help"])
    assert result.exit_code == 0
    assert typer.unstyle(result.output) == snapshot("""\
                                                                                \n\
 Usage: psift open [OPTIONS] SOURCE                                             \n\
                                                                                \n\
 Open a file in psift.                                                          \n\
                                                                                \n\
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    source      PATH  Source file to open. [required]                       │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help  -h        Show this message and exit.                                │
╰──────────────────────────────────────────────────────────────────────────────╯

""")


def test_version_help() -> None:
    result = runner.invoke(cli, ["version", "--help"])
    assert result.exit_code == 0
    assert typer.unstyle(result.output) == snapshot("""\
                                                                                \n\
 Usage: psift version [OPTIONS]                                                 \n\
                                                                                \n\
 Show psift version.                                                            \n\
                                                                                \n\
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help  -h        Show this message and exit.                                │
╰──────────────────────────────────────────────────────────────────────────────╯

""")


def test_short_help_alias() -> None:
    long_form = runner.invoke(cli, ["--help"])
    short_form = runner.invoke(cli, ["-h"])
    assert long_form.exit_code == 0
    assert short_form.exit_code == 0
    assert long_form.output == short_form.output


@pytest.mark.parametrize("args", [["version"], ["--version"], ["-V"]])
def test_version_output(args: list[str]) -> None:
    result = runner.invoke(cli, args)
    assert result.exit_code == 0
    assert result.output == snapshot("psift 0.0.2\n")
