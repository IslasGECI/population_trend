import pandas as pd


def write_burrows_by_species_and_island(data_path, species, island, output_path):
    data = pd.read_csv(data_path)
    filtered = filter_by_species_and_island(data, species, island)
    filtered.to_csv(output_path, index=False)


def filter_by_species_and_island(data: pd.DataFrame, species: str, island: str):
    filtered_by_species = filter_by_species(data, species)
    return filter_data_by_islet(filtered_by_species, island)


def filter_by_species(data: pd.DataFrame, species: str):
    return data[data.Nombre_en_ingles == species]


def filter_data_by_islet(df, islet):
    return df[df.Isla == islet]
