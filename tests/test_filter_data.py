from population_trend import filter_by_species, filter_by_species_and_island
import pandas as pd


data = pd.read_csv("tests/data/dcco_laal_gumu_burrows_data.csv")
species = "Laysan Albatross"


def test_filter_by_species_and_island():
    island = "Guadalupe"
    filter_by_species_and_island(data, species, island)


def test_filter_by_species():
    obtained_df = filter_by_species(data, species)
    obtained_len = len(obtained_df)
    expected_len = 21
    assert obtained_len == expected_len
