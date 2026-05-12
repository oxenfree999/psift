"""Bottom status bar showing the loaded source's name and shape."""

from rich.text import Text
from textual.widgets import Static

ACCENT = "#f9e2af"


class StatusBar(Static):
    """One-line bar: ``name · N cols · M rows``."""

    def __init__(self) -> None:
        """Start with an empty bar. `set_source` fills it once data lands."""
        super().__init__()
        self._text = Text()
        self.styles.height = 1
        self.styles.padding = (0, 1)

    @property
    def current_text(self) -> Text:
        """Return the rendered Rich Text the bar is currently displaying."""
        return self._text

    def set_source(self, name: str, *, rows: int, columns: int, loaded: int | None = None) -> None:
        """Render the bar. With `loaded < rows`, show `loaded / rows`."""
        text = Text()
        text.append(name)
        text.append(" · ", style="dim")
        text.append(str(columns), style=f"bold {ACCENT}")
        text.append(" cols")
        text.append(" · ", style="dim")
        if loaded is not None and loaded < rows:
            text.append(f"{loaded:,}", style=f"bold {ACCENT}")
            text.append(" / ", style="dim")
            text.append(f"{rows:,}", style=f"bold {ACCENT}")
        else:
            text.append(f"{rows:,}", style=f"bold {ACCENT}")
        text.append(" rows")
        self._text = text
        self.update(text)
