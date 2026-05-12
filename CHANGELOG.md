# Changelog

## v0.0.2 (2026-05-11)

### Added

- Add Polars as a runtime dependency.
- Add source metadata and dtype categorization.
- Add lazy CSV, TSV, Parquet, and Arrow IPC loaders plus in-memory loaders.
- Add the open screen and supporting widgets (`PsiftApp`, `OpenScreen`, `VirtualTable`, `StatusBar`).
- Add `psift open <source>` to load one filesystem source and launch the app.
- Open large sources without an eager full-table load by painting a preview head first and streaming the rest in the background, with `loaded / total` shown in the status bar.

## v0.0.1 (2026-04-29)

### Added

- Add the CLI entry point with `psift version`.
- Add `psift doctor` for environment diagnostics.
- Add the CI pipeline with ruff, ty, pytest, and just.
- Add the Python version pin and lockfile.
- Add baseline project docs (README, CONTRIBUTING, SECURITY, code of conduct).
