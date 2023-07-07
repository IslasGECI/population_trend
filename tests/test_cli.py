from population_trend import (
    app,
    plot_population_trend,
    write_burrows_by_species_and_island,
)
import os
import pandas as pd
from typer.testing import CliRunner
import hashlib


runner = CliRunner()

data_path = "tests/data/dcco_laal_gumu_burrows_data.csv"
data = pd.read_csv(data_path)
species = "Laysan Albatross"
island = "Guadalupe"
output_path = "tests/data/laal_guadalupe.csv"
intervals_path = "tests/data/gumu_guadalupe_boostrap_intervals.json"
output_figure = "tests/data/figure.png"


def test_app():
    result = runner.invoke(
        app,
        ["plot-population-trend", "--help"],
    )
    assert "XX" not in result.stdout
    assert "[default: Guadalupe]" in result.stdout
    assert "[default: Maxima_cantidad_nidos]" in result.stdout
    result = runner.invoke(
        app,
        [
            "plot-population-trend",
            "--data-path",
            data_path,
            "--intervals-path",
            intervals_path,
            "--island",
            "Guadalupe",
            "--variable-of-interest",
            "Maxima_cantidad_nidos",
            "--output-path",
            output_figure,
        ],
    )
    assert result.exit_code == 0
    result = runner.invoke(
        app,
        ["write-burrows-by-species-and-island", "--help"],
    )
    assert "[default: data/processed/subset_burrows_data.csv]" in result.stdout
    assert "[default: Guadalupe Murrelet]" in result.stdout
    assert "[default: Guadalupe]" in result.stdout
    assert "[default: data/processed/gumu_guadalupe_burrows.csv]" in result.stdout
    result = runner.invoke(
        app,
        [
            "write-burrows-by-species-and-island",
            "--data-path",
            data_path,
            "--species",
            species,
            "--island",
            island,
            "--output-path",
            output_path,
        ],
    )
    assert result.exit_code == 0
    result = runner.invoke(
        app,
        ["--help"],
    )
    assert "XX" not in result.stdout

    data_gumu_path = "tests/data/gumu_guadalupe_data.csv"
    output_json = "tests/data/gumu_guadalupe_tests.json"
    result = runner.invoke(
        app,
        [
            "write-bootstrap-intervals-json",
            "--data-path",
            data_gumu_path,
            "--blocks-length",
            3,
            "--bootstrap-number",
            10,
            "--output-path",
            output_json,
        ],
    )
    assert result.exit_code == 0


def test_write_burrows_by_species_and_island():
    write_burrows_by_species_and_island(data_path, species, island, output_path)
    obtained_csv = pd.read_csv(output_path)
    obtained_columns = len(obtained_csv.columns)
    expected_columns = 12
    assert obtained_columns == expected_columns
