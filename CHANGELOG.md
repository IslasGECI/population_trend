# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [5.7.2] - 2024-02-08

### Fixed
- print p-values format

## [5.7.1] - 2024-02-08

### Fixed
- Rephrase hypothesis tests statement
- Print p-values without zero before decimal point

## [5.7.0] - 2024-02-02

### Added
- Add english version of hypothesis test: "hypotheris_tests_statement_latex_en"

### Changed
- json key for spanish hypothesis test: "hypotesis_test_statement_latex" -> "hypothesis_test_statement_latex_sp"

## [5.6.5] - 2024-02-02

### Fixed

- Fix latex symbols: "\gt" -> ">"

## [5.6.4] - 2024-02-02

### Fixed

- JSON string format 

## [5.6.3] - 2024-02-01

### Fixed

- Write statement of hypotesis test

## [5.6.2] - 2024-02-01

### Added

- Add statement of hypotesis test

## [5.6.1] - 2023-12-08


### Fixed

- Command `plot-growth-rate` and `plot_population_trend()` function write figures with transparent background

## [5.6.0] - 2023-12-07

### Added

- Added command `plot-growth-rate` to cli

## [5.5.0] - 2023-11-30

### Added

- Added command `write-regional-trends` to cli
- Added badges to readme

### Fixed

- Fix `tests/test_Population_trend.py` to pass check

### Changed

- Use properties in class `Bootstrap_from_time_series`
- Split `test_app()`
- Improve cli formating using Rich 

### Removed


## [5.4.0] - 2023-07-14

### Added


### Fixed


[unreleased]: https://github.com/IslasGECI/population_trend/compare/v5.5.0...HEAD
[5.5.0]: https://github.com/IslasGECI/population_trend/compare/v5.4.0...v5.5.0
[0.0.1]: https://github.com/IslasGECI/population_trend/releases/tag/v0.0.1
