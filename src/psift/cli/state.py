"""Global CLI state passed to all subcommands via ctx.obj."""

from enum import IntEnum


class ExitCode(IntEnum):
    """Process exit codes."""

    SUCCESS = 0
    ERROR = 1
    USAGE = 2
