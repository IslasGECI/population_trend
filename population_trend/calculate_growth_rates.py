from bootstrapping_tools import (
    bootstrap_from_time_series,
    calculate_p_values,
    get_bootstrap_deltas,
    lambda_calculator,
    power_law,
    AbstractSeriesBootstrapper,
    Bootstrap_from_time_series_parametrizer,
)
from matplotlib.ticker import MaxNLocator

import json
import matplotlib.pyplot as plt
import numpy as np


def calculate_porcentual_diff(x, y):
    return 100 * (x - y) / y


def generate_number_and_season_string(number, season):
    return "{} ({})".format(
        number,
        season,
    )


def calculate_seasons_intervals(seasons):
    years = []
    first_index = 0
    for index in np.where(np.diff(seasons) != 1)[0]:
        if seasons[first_index] == seasons[index]:
            years.append(f"{seasons[index]}")
        else:
            years.append(f"{seasons[first_index]}-{seasons[index]}")
        first_index = index + 1
    years.append(f"{seasons[first_index]}-{seasons[-1]}")
    return years


def calculate_interest_numbers(cantidad_nidos, model):
    first_number = generate_number_and_season_string(
        cantidad_nidos["Maxima_cantidad_nidos"].iloc[0],
        cantidad_nidos["Temporada"].iloc[0],
    )
    first_number_calculated = generate_number_and_season_string(
        model.iloc[0], cantidad_nidos["Temporada"].iloc[0]
    )
    last_number = "{{{:,.0f}}} ({})".format(
        cantidad_nidos["Maxima_cantidad_nidos"].iloc[-1],
        int(cantidad_nidos["Temporada"].iloc[-1]),
    )
    last_number_calculated = generate_number_and_season_string(
        model.iloc[-1],
        cantidad_nidos["Temporada"].iloc[-1],
    )
    return first_number, first_number_calculated, last_number, last_number_calculated


def calculate_percent_diff_in_seasons(cantidad_nidos, model):
    if cantidad_nidos["Maxima_cantidad_nidos"].iloc[0] == 0:
        porcentaje_cambio = calculate_porcentual_diff(model.iloc[-1], model.iloc[0])
    else:
        porcentaje_cambio = calculate_porcentual_diff(
            model.iloc[-1], cantidad_nidos["Maxima_cantidad_nidos"].iloc[0]
        )
    return porcentaje_cambio


def fit_population_model(seasons_series, data_series):
    parameters = lambda_calculator(seasons_series, data_series)
    model = power_law(
        seasons_series - seasons_series.iloc[0],
        parameters[0],
        parameters[1],
    )
    return model


class LambdasBootstrapper(AbstractSeriesBootstrapper):
    def __init__(self, bootstrap_parametrizer):
        self.bootstrap_config = bootstrap_parametrizer.parameters
        self.data_series = self.bootstrap_config["dataframe"][self.bootstrap_config["column_name"]]
        self.season_series = self.bootstrap_config["dataframe"]["Temporada"]
        self.parameters_distribution, _ = self.get_parameters_distribution()

    def get_parameters_distribution(self):
        lambdas_n0_distribution, intervals = bootstrap_from_time_series(**self.bootstrap_config)
        return lambdas_n0_distribution, intervals

    def get_distribution(self):
        return self.parameters_distribution

    def get_inferior_central_and_superior_limit(self):
        inferior_limit, central, superior_limit = get_bootstrap_deltas(
            self.interval_lambdas, **{"decimals": 2}
        )
        return inferior_limit, central, superior_limit

    def fit_population_model(self):
        model = fit_population_model(self.season_series, self.data_series)
        return model

    def generate_season_interval(self):
        return "({}-{})".format(
            self.season_series.min(axis=0),
            self.season_series.max(axis=0),
        )

    def get_monitored_seasons(self):
        monitored_seasons = np.sort(self.season_series.astype(int).unique())
        if len(monitored_seasons) == 1:
            return f"{monitored_seasons[0]}"
        else:
            seasons_intervals = calculate_seasons_intervals(monitored_seasons)
            return ",".join(seasons_intervals)

    def save_intervals(self, output_path):
        json_dict = self.get_parameters_dictionary()
        json_dict["lambda_latex_interval"] = json_dict.pop("main_parameter_latex_interval")
        with open(output_path, "w") as file:
            json.dump(json_dict, file)


def calculate_growth_rates_table(bootstrap: Bootstrap_from_time_series_parametrizer):
    bootstraper = LambdasBootstrapper(bootstrap)
    df = bootstrap.parameters["dataframe"]
    model = bootstraper.fit_population_model()
    inferior_limit, central, superior_limit = bootstraper.get_inferior_central_and_superior_limit()
    lambda_latex_string = bootstraper.lambda_latex_interval
    bootstrap_distribution = bootstraper.get_distribution()
    lambdas_distribution = [interval[0] for interval in bootstrap_distribution]
    p_value_mayor, p_value_menor = calculate_p_values(lambdas_distribution)
    intervalo = bootstraper.generate_season_interval()
    monitored_seasons = bootstraper.get_monitored_seasons()
    porcentaje_cambio = calculate_percent_diff_in_seasons(df, model)
    (
        first_number,
        _,
        last_number,
        last_number_calculated,
    ) = calculate_interest_numbers(df, model)
    return [
        intervalo,
        first_number,
        last_number,
        last_number_calculated,
        lambda_latex_string,
        df["Latitud"].iloc[0],
        central,
        f"-{inferior_limit}",
        f"+{superior_limit}",
        f"{{{int(porcentaje_cambio):,}}}",
        p_value_mayor,
        p_value_menor,
        monitored_seasons,
    ]


def set_axis_plot_config(ax):
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    fontsize = 20
    plt.yticks(rotation=90, size=fontsize)
    locs_x, _ = plt.xticks()
    locs_y, _ = plt.yticks()
    plt.xticks(locs_x[1:], size=fontsize)
    plt.xlim(locs_x[0], locs_x[-1])
    plt.ylim(0, locs_y[-1])
    ax.set_xlabel("Año", size=fontsize, labelpad=10)
    plt.ylabel("Cantidad de parejas reproductoras", size=fontsize)
