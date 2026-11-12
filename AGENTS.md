# AGENTS.md

## Public interface

The public interface is the CLI commands registred on `population_trend.cli:app` and exposed as `population-trend` through `[tool.flit.scripts]` in `pyproject.toml`, plus the functions re-exported from `population_trend/__init__.py`. Treat other internal helpers as developer-only unless the interface definition changes.

## Developer commands

- Run `make setup` before any other target: it cleans caches and installs the package editable. The Docker image installs only lint and test tools, not the package.
- `make check` runs `black --check`, `flake8`, and `mypy` over `population_trend` and `tests`; black and flake8 use line length 100.
- `make coverage` runs `pytest --cov=population_trend --cov-report=xml` and writes `coverage.xml`.
- `make tests` runs `pytest --verbose`.
- `make mutants` runs `mutmut run` over `population_trend` and falls back to `mutmut html`.
- `make linter` runs pylint with the project disables.
- `make red`, `make green`, and `make refactor` format, run pytest, then commit or `git restore`; `tdd_current_test_file` defaults to `tests/`.
- `make init` runs `init_git`, `setup`, and `tests`; `init_git` sets the GECI git identity and adds `/workdir` as a safe directory.

## Toolchain

- Build backend is flit; the package version lives in `population_trend/__init__.py` as `__version__`.
- Requires Python >= 3.9; `Dockerfile` uses 3.10 and the CI PyPI build step uses 3.9.
- Runtime dependencies are pinned in `pyproject.toml`; `bootstrapping-tools==3.*` supplies `compute_lambda_bootstrapped_intervals_from_time_series`, used by `calculate_growth_rates.py`.
- `population_trend/__init__.py` re-exports modules with star imports, so import public names from the package root.

## Tests

- Tests use `typer.testing.CliRunner` for CLI checks and `pytest-mpl` image comparisons against `tests/baseline/`.
- Tests write outputs into `tests/data/` and the repository root; generated PNG and JSON files are untracked, so a dirty tree after `make tests` is expected.
- Add a CLI test when adding a command; `tests/test_cli.py` checks help output and command behaviour.

## CI

- `.github/workflows/actions.yml` builds the Docker image, runs `make check` and `make coverage`, uploads to Codecov, force-pushes the `latest` tag, and publishes to PyPI and Docker Hub on `develop`.
- A separate `mutants` job runs `make mutants` and uploads `html/`.
