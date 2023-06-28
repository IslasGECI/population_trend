from population_trend import (
    app,
    plot_population_trend,
    write_burrows_by_species_and_island,
)
import os
import pandas as pd
from typer.testing import CliRunner


runner = CliRunner()

data_path = "tests/data/dcco_laal_gumu_burrows_data.csv"
data = pd.read_csv(data_path)
species = "Laysan Albatross"
island = "Guadalupe"
output_path = "tests/data/laal_guadalupe.csv"


def test_app():
    result = runner.invoke(
        app,
        [
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


def test_write_burrows_by_species_and_island():
    write_burrows_by_species_and_island(data_path, species, island, output_path)
    obtained_csv = pd.read_csv(output_path)
    obtained_columns = len(obtained_csv.columns)
    expected_columns = 12
    assert obtained_columns == expected_columns


def test_plot_population_trend():
    data_path = "tests/data/gumu_guadalupe_data.csv"
    intervals_path = "tests/data/gumu_guadalupe_boostrap_intervals.json"
    output_path = "tests/data/gumu_guadalupe_population_trend.png"
    if os.path.exists(output_path):
        os.remove(output_path)
    plot_population_trend(data_path, intervals_path, output_path)
    assert os.path.exists(output_path)
