from population_trend import filter_by_species
import pandas as pd


def test_filter_by_species():
    data = pd.read_csv("tests/data/dcco_laal_gumu_burrows_data.csv")
    species = "Laysan Albatross"
    obtained_df = filter_by_species(data, species)
    obtained_len = len(obtained_df)
    expected_len = 21
    assert obtained_len == expected_len
