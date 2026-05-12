"""psift CLI entry point."""

import json
import sys
from pathlib import Path
from typing import Annotated

import typer

from psift.cli.doctor import format_text, get_system_info
from psift.cli.state import ExitCode
from psift.core import open_source
from psift.tui import PsiftApp
from psift.version import VERSION

cli = typer.Typer(
    name="psift",
    help="A terminal tabular data explorer.",
    no_args_is_help=True,
    context_settings={"help_option_names": ["--help", "-h"]},
)


def _version_callback(value: bool) -> None:
    """Print the version and exit when ``--version`` is passed."""
    if value:
        print(f"psift {VERSION}")
        raise typer.Exit(ExitCode.SUCCESS)


@cli.callback()
def _main(
    version: Annotated[
        bool | None, typer.Option("--version", "-V", callback=_version_callback, is_eager=True, help="Show version.")
    ] = None,
) -> None:
    """Hold subcommand routing. Typer collapses single-command apps without it."""


@cli.command()
def doctor(
    json_flag: Annotated[bool, typer.Option("--json", help="Output JSON instead of text.")] = False,
) -> None:
    """Check psift environment and report status."""
    info = get_system_info()
    if json_flag:
        print(json.dumps(info, indent=2))
    else:
        print(format_text(info))


@cli.command(name="open")
def open_cmd(
    source: Annotated[Path, typer.Argument(help="Source file to open.")],
) -> None:
    """Open a file in psift."""
    try:
        loaded = open_source(source)
    except (FileNotFoundError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        raise typer.Exit(ExitCode.ERROR) from exc
    PsiftApp(loaded).run()


@cli.command()
def version() -> None:
    """Show psift version."""
    print(f"psift {VERSION}")
