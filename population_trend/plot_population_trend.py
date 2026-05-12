from population_trend.population_growth_model import (
    Plotter_Population_Trend_Model,
    Population_Trend_Model,
)

import pandas as pd


def _plot_population_trend(
    fit_data: pd.DataFrame,
    intervals_json: dict,
    island: str = "Guadalupe",
    variable_of_interest: str = "Maxima_cantidad_nidos",
    tick_mode: str = "full",
    show_legend: bool = True,
):
    """Shared implementation for rendering population trend plots."""
    lambda_latex = intervals_json["lambda_latex_interval"]

    Modelo_Tendencia_Poblacional = Population_Trend_Model(
        fit_data, intervals_json, variable_of_interest
    )
    Graficador = Plotter_Population_Trend_Model(
        fit_data, Modelo_Tendencia_Poblacional, tick_mode, show_legend=show_legend
    )
    Graficador.plot_smooth()
    Graficador.plot_model()
    Graficador.plot_data()
    legend_mpl_object = Graficador.set_legend_location(island)
    Graficador.plot_growth_rate_interval(legend_mpl_object, lambda_latex)
    return Graficador
