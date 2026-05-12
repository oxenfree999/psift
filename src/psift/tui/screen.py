"""Open screen for psift."""

import asyncio

import polars as pl
from textual.app import ComposeResult
from textual.screen import Screen

from psift.core.source import Source
from psift.tui.widgets.status_bar import StatusBar
from psift.tui.widgets.virtual_table import VirtualTable

# First-paint preview cap. Not a final-view truncation.
_INITIAL_PREVIEW_ROWS = 500


class OpenScreen(Screen):
    """Render one loaded `Source` in a `DataTable` plus a thin status bar."""

    def __init__(self, source: Source) -> None:
        """Initialise the screen with the loaded source."""
        super().__init__()
        self.source = source
        self.table = VirtualTable()
        self.status_bar = StatusBar()
        self.table.styles.height = "1fr"
        self._total_rows: int = 0
        self._loaded_rows: int = 0
        self._load_task: asyncio.Task[None] | None = None

    def compose(self) -> ComposeResult:
        """Yield the table on top and the status bar at the bottom."""
        yield self.table
        yield self.status_bar

    def on_mount(self) -> None:
        """Paint the preview head and stream the rest in the background."""
        preview = self.source.lf.head(_INITIAL_PREVIEW_ROWS).collect()
        total = self.source.lf.select(pl.len()).collect()
        if not isinstance(preview, pl.DataFrame) or not isinstance(total, pl.DataFrame):
            msg = f"Unexpected polars collect result: {type(preview).__name__}, {type(total).__name__}"
            raise TypeError(msg)
        self._total_rows = int(total.item())
        self._loaded_rows = preview.height
        self.table.populate(preview)
        self.status_bar.set_source(
            self.source.name,
            rows=self._total_rows,
            columns=preview.width,
            loaded=self._loaded_rows,
        )
        if self._loaded_rows < self._total_rows:
            self._load_task = asyncio.create_task(self._stream_full_frame())

    def on_unmount(self) -> None:
        """Cancel any in-flight background load when the screen unmounts."""
        task = self._load_task
        self._load_task = None
        if task is not None and not task.done():  # pragma: no cover
            task.cancel()

    async def _stream_full_frame(self) -> None:
        """Materialise the full source off-thread and swap it into the table."""
        full = await asyncio.to_thread(self.source.lf.collect)
        if self._load_task is not asyncio.current_task():  # pragma: no cover
            return
        if not isinstance(full, pl.DataFrame):  # pragma: no cover
            self._load_task = None
            return
        self.table.populate(full)
        self._loaded_rows = full.height
        self.status_bar.set_source(
            self.source.name,
            rows=self._total_rows,
            columns=full.width,
            loaded=self._loaded_rows,
        )
        self._load_task = None
