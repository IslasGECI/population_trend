from population_trend import (
    plot_population_trend,
    write_burrows_by_species_and_island,
)
import pandas as pd


data_path = "tests/data/dcco_laal_gumu_burrows_data.csv"
data = pd.read_csv(data_path)
species = "Laysan Albatross"
island = "Guadalupe"


def test_write_burrows_by_species_and_island():
    output_path = "tests/data/laal_guadalupe.csv"
    write_burrows_by_species_and_island(data_path, species, island, output_path)
    obtained_csv = pd.read_csv(output_path)
    obtained_columns = len(obtained_csv.columns)
    expected_columns = 12
    assert obtained_columns == expected_columns


def test_plot_population_trend():
    gumu_data_path = "tests/data/gumu_guadalupe_data.csv"
    intervals_path = "tests/data/gumu_guadalupe_boostrap_intervals.json"
    output_path = "tests/data/gumu_guadalupe_population_trend.png"
    plot_population_trend(gumu_data_path, intervals_path, output_path)
