from population_trend import (
    filter_by_species,
    filter_by_species_and_island,
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


def test_filter_by_species_and_island():
    obtained_df = filter_by_species_and_island(data, species, island)
    obtained_len = len(obtained_df)
    expected_len = 15
    assert obtained_len == expected_len


def test_filter_by_species():
    obtained_df = filter_by_species(data, species)
    obtained_len = len(obtained_df)
    expected_len = 21
    assert obtained_len == expected_len
