# Fix, lint, type-check, and test
default: format lint test

# Auto-fix formatting and lint issues
format:
    uv run ruff format .
    uv run ruff check --fix .

# Static analysis: lint, format check, and type-check
lint:
    uv run ruff check .
    uv run ruff format --check .
    uv run ty check

# Run the test suite
test *args:
    uv run pytest --cov --cov-report=term-missing {{ args }}

# Accept changed, new, and reformatted snapshot values
snap:
    uv run pytest --inline-snapshot=create,fix,update
