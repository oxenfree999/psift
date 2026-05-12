"""Environment health checks for psift doctor."""

import os
import platform
from importlib.metadata import PackageNotFoundError, version
from typing import Any

from psift.version import VERSION

LABEL_WIDTH = 14

_TRACKED_RUNTIMES = ("typer",)
_TRUECOLOR_VALUES = frozenset({"truecolor", "24bit"})


def _runtime_versions() -> dict[str, bool]:
    """Return availability of each tracked runtime as a name-to-bool map."""
    available: dict[str, bool] = {}
    for name in _TRACKED_RUNTIMES:
        try:
            version(name)
        except PackageNotFoundError:
            available[name] = False
        else:
            available[name] = True
    return available


def _terminal_capabilities() -> dict[str, bool]:
    """Return terminal capability flags derived from environment variables."""
    colorterm = os.environ.get("COLORTERM", "").lower()
    return {"truecolor": colorterm in _TRUECOLOR_VALUES}


def get_system_info() -> dict[str, Any]:
    """Collect environment information for ``psift doctor``."""
    return {
        "psift": {"version": VERSION},
        "python": {
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
        },
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
        "runtime": _runtime_versions(),
        "terminal": _terminal_capabilities(),
    }


def format_text(info: dict[str, Any]) -> str:
    """Format system info as column-aligned human-readable text."""
    py = info["python"]
    plat = info["platform"]
    lines = [
        f"{'psift':<{LABEL_WIDTH}} {info['psift']['version']}",
        f"{'python':<{LABEL_WIDTH}} {py['version']} ({py['implementation']})",
        f"{'platform':<{LABEL_WIDTH}} {plat['system']} {plat['release']} ({plat['machine']})",
        "",
        "runtime:",
    ]
    for name, available in info["runtime"].items():
        status = "available" if available else "not installed"
        lines.append(f"  {name:<{LABEL_WIDTH - 2}} {status}")
    lines.append("")
    lines.append("terminal:")
    for cap, on in info["terminal"].items():
        status = "yes" if on else "no"
        lines.append(f"  {cap:<{LABEL_WIDTH - 2}} {status}")
    return "\n".join(lines)
