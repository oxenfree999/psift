"""Top-level Textual application for psift."""

from textual.app import App

from psift.core.source import Source
from psift.tui.screen import OpenScreen
from psift.version import VERSION


class PsiftApp(App):
    """Top level psift app. Pushes `OpenScreen` and lets the user drive."""

    TITLE = f"psift {VERSION}"

    def __init__(self, source: Source) -> None:
        """Initialise the app with the source the user opened."""
        super().__init__()
        self.source = source

    def on_mount(self) -> None:
        """Push the open screen onto the stack."""
        self.push_screen(OpenScreen(self.source))
