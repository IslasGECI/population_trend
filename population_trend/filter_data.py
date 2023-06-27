import pandas as pd

from population_trend.population_growth_model import filter_data_by_islet


def filter_by_species_and_island(data: pd.DataFrame, species: str, island: str):
    filtered_by_species = filter_by_species(data, species)
    return filter_data_by_islet(filtered_by_species, island)


def filter_by_species(data: pd.DataFrame, species: str):
    return data[data.Nombre_en_ingles == species]
