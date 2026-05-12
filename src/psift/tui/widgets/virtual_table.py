"""Thin DataTable wrapper: vim-key bindings plus a populate helper."""

from typing import ClassVar

import polars as pl
from rich.text import Text
from textual.binding import Binding
from textual.widgets import DataTable

NULL_DISPLAY = "null"
NULL_STYLE = "dim"


class VirtualTable(DataTable):
    """``DataTable`` with ``j`` / ``k`` / ``h`` / ``l`` aliases."""

    BINDINGS: ClassVar[list[Binding]] = [
        Binding("j", "cursor_down", show=False),
        Binding("k", "cursor_up", show=False),
        Binding("h", "cursor_left", show=False),
        Binding("l", "cursor_right", show=False),
    ]

    def populate(self, df: pl.DataFrame) -> None:
        """Replace the table contents with rows from *df*.

        Null cells render as a dim ``"null"`` token so they read distinctly
        from a literal string ``"null"`` value in the source.
        """
        self.clear(columns=True)
        self.add_columns(*df.columns)
        for row in df.iter_rows():
            cells = [Text(NULL_DISPLAY, style=NULL_STYLE) if value is None else str(value) for value in row]
            self.add_row(*cells)
