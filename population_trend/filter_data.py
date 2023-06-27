import pandas as pd


def filter_by_species(data: pd.DataFrame, species: str):
    return data[data.Nombre_en_ingles == species]
