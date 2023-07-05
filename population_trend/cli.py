from population_trend.filter_data import filter_by_species_and_island
from population_trend.population_growth_model import (
    Population_Trend_Model,
    Plotter_Population_Trend_Model,
)
from population_trend.calculate_growth_rates import (
    Bootstrap_from_time_series_parameterizer,
    Bootstrap_from_time_series,
)
import pandas as pd
import typer
import json

app = typer.Typer(help="Write filtered burrows data by species and island")


@app.command(help="Write json with bootstrap intervals")
def write_bootstrap_intervals_json(
    data_path: str = "data/processed/gumu_guadalupe_burrows.csv",
    blocks_length: int = 3,
    output_path: str = "reports/non-tabular/gumu_guadalupe_boostrap_intervals.json",
):
    data = pd.read_csv(data_path)
    parametrizer = Bootstrap_from_time_series_parameterizer(blocks_length=blocks_length)
    parametrizer.set_data(data)
    bootstrap = Bootstrap_from_time_series(parametrizer)
    bootstrap.save_intervals(output_path)


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


@app.command(help="Plot population trend")
def plot_population_trend(
    data_path: str = "",
    intervals_path: str = "",
    island: str = "Guadalupe",
    variable_of_interest: str = "Maxima_cantidad_nidos",
    output_path=None,
):
    fit_data = pd.read_csv(data_path)
    with open(intervals_path, "r") as read_file:
        intervals_json = json.load(read_file)
    intervals = intervals_json["intervals"]
    lambda_latex = intervals_json["lambda_latex_interval"]

    Modelo_Tendencia_Poblacional = Population_Trend_Model(fit_data, intervals, variable_of_interest)
    Graficador = Plotter_Population_Trend_Model(fit_data)
    Graficador.plot_smooth(Modelo_Tendencia_Poblacional)
    Graficador.plot_model(Modelo_Tendencia_Poblacional)
    Graficador.plot_data(variable_of_interest)
    legend_mpl_object = Graficador.set_legend_location(island)
    Graficador.set_x_lim()
    Graficador.set_y_lim(fit_data[variable_of_interest])
    Graficador.set_labels()
    Graficador.set_ticks()
    Graficador.draw()
    Graficador.plot_growth_rate_interval(legend_mpl_object, lambda_latex)
    Graficador.savefig(island, output_path)
