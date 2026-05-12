"""Runtime version string read from installed package metadata."""

from importlib.metadata import version

VERSION = version("psift")
