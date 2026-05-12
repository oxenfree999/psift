"""Pilot smoke tests for psift open."""

import asyncio
from collections.abc import Callable

import pytest

from psift.core.source import Source
from psift.tui.app import PsiftApp
from psift.tui.screen import OpenScreen


async def test_app_launches_and_loads_data(tiny_source: Source) -> None:
    app = PsiftApp(tiny_source)
    async with app.run_test(size=(120, 30)) as pilot:
        await pilot.pause()
        screen = app.screen
        assert isinstance(screen, OpenScreen)
        assert screen.table.row_count == 10
        bar_text = screen.status_bar.current_text.plain
        assert bar_text.startswith("tiny")
        assert "6 cols" in bar_text
        assert "10 rows" in bar_text


async def test_vim_keys_move_cursor_in_all_four_directions(tiny_source: Source) -> None:
    app = PsiftApp(tiny_source)
    async with app.run_test(size=(120, 30)) as pilot:
        await pilot.pause()
        screen = app.screen
        assert isinstance(screen, OpenScreen)
        table = screen.table
        assert table.cursor_row == 0
        assert table.cursor_column == 0

        await pilot.press("j")
        await pilot.pause()
        await pilot.press("j")
        await pilot.pause()
        assert table.cursor_row == 2

        await pilot.press("k")
        await pilot.pause()
        assert table.cursor_row == 1

        await pilot.press("l")
        await pilot.pause()
        await pilot.press("l")
        await pilot.pause()
        assert table.cursor_column == 2

        await pilot.press("h")
        await pilot.pause()
        assert table.cursor_column == 1


async def test_large_source_streams_full_frame_in_background(
    large_source: Source, monkeypatch: pytest.MonkeyPatch
) -> None:
    block = asyncio.Event()
    real_to_thread = asyncio.to_thread

    async def gated_to_thread(func: Callable[..., object], /, *args: object, **kwargs: object) -> object:
        await block.wait()
        return await real_to_thread(func, *args, **kwargs)

    monkeypatch.setattr(asyncio, "to_thread", gated_to_thread)

    app = PsiftApp(large_source)
    async with app.run_test(size=(120, 30)) as pilot:
        await pilot.pause()
        screen = app.screen
        assert isinstance(screen, OpenScreen)
        assert screen.table.row_count == 500
        bar_text = screen.status_bar.current_text.plain
        assert bar_text.startswith("large")
        assert "500 / 10,000" in bar_text

        block.set()
        for _ in range(50):
            if screen.table.row_count == 10_000:
                break
            await pilot.pause()

        assert screen.table.row_count == 10_000
        bar_text = screen.status_bar.current_text.plain
        assert "10,000 rows" in bar_text
        assert "/" not in bar_text
