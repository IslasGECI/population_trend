from population_trend.filter_data import filter_by_species_and_island
import pandas as pd
import typer

app = typer.Typer(help="Write filtered burrows data by species and island")


@app.command(help="Write csv with ouput-path")
def write_burrows_by_species_and_island(
    data_path: str = "data/processed/subset_burrows_data.csv",
    species: str = "Guadalupe Murrelet",
    island: str = "Guadalupe",
    output_path: str = "data/processed/gumu_guadalupe_burrows.csv",
):
    data = pd.read_csv(data_path)
    filtered = filter_by_species_and_island(data, species, island)
    filtered.to_csv(output_path, index=False)
