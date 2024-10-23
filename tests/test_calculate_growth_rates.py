from numpy.testing import assert_array_almost_equal
import pandas as pd
import pytest
import json
import os
import population_trend as lam
from bootstrapping_tools import Bootstrap_from_time_series_parametrizer
import geci_plots as gp

import matplotlib.pyplot as plt


nidos_array = [
    {"Temporada": 2014, "Maxima_cantidad_nidos": 283},
    {"Temporada": 2015, "Maxima_cantidad_nidos": 126},
    {"Temporada": 2016, "Maxima_cantidad_nidos": 395},
    {"Temporada": 2017, "Maxima_cantidad_nidos": 344},
    {"Temporada": 2018, "Maxima_cantidad_nidos": 921},
    {"Temporada": 2019, "Maxima_cantidad_nidos": 847},
]


def get_df(file_path):
    with open(file_path) as file:
        df = pd.read_csv(file)
    return df


df = get_df("tests/data/dcco_laal_gumu_burrows_data.csv")
laal = df[df["Nombre_en_ingles"] == "Laysan Albatross"]
bootstrap_number = 10
parametrizer = Bootstrap_from_time_series_parametrizer(blocks_length=2, N=bootstrap_number)
parametrizer.set_data(laal)
bootstraper = lam.LambdasBootstrapper(parametrizer)


def test_save_intervals():
    output_path = "tests/data/laal_intervals.json"
    bootstraper.save_intervals(output_path)
    with open(output_path) as json_file:
        obtained_json = json.load(json_file)
    obtained_fields = list(obtained_json.keys())
    expected_fields = [
        "intervals",
        "lambda_latex_interval",
        "p-values",
        "bootstrap_intermediate_distribution",
    ]
    assert set(obtained_fields) == set(expected_fields)
    expected_intervals = [[1.1097, 128.85392], [1.2094, 68.65764], [1.4272, 4.56072]]
    assert_array_almost_equal(obtained_json["intervals"], expected_intervals, decimal=5)
    expected_latex_interval = "1.21 (1.11 - 1.43)"
    assert obtained_json["lambda_latex_interval"] == expected_latex_interval
    obtained_p_minor_value = obtained_json["p-values"][0]
    assert obtained_p_minor_value >= 0
    obtained_p_major_value = obtained_json["p-values"][1]
    assert obtained_p_major_value <= 1
    obtained_min_lambda = min(obtained_json["bootstrap_intermediate_distribution"])
    assert obtained_min_lambda[0] >= expected_intervals[0][0]
    obtained_max_lambda = max(obtained_json["bootstrap_intermediate_distribution"])
    assert obtained_max_lambda[0] <= expected_intervals[2][0]
    os.remove(output_path)


def test_intervals_from_p_values_and_alpha():
    dcco = df[df["Nombre_en_ingles"] == "Double-crested Cormorant"]
    parametrizer = lam.Bootstrap["testing"]
    parametrizer.set_data(dcco)
    assert parametrizer.parameters["alpha"] == 0.05
    bootstraper = lam.LambdasBootstrapper(parametrizer)
    obtained_intervals = bootstraper.intervals
    obtained_len_intervals = len(obtained_intervals)
    expected_len_intervals = 3
    assert obtained_len_intervals == expected_len_intervals
    expected_intervals = [
        (1.03555254967221, 56.72689275689199),
        (1.2199265239402008, 14.422599452094458),
        (9.496750484649498, 2.419173122070242e-07),
    ]
    expected_intervals = [
        [1.03555e00, 5.67269e01],
        [1.18278e00, 2.89561e01],
        [9.49983e00, 2.41214e-07],
    ]
    assert_array_almost_equal(obtained_intervals, expected_intervals, decimal=4)


def test_calculate_interest_numbers():
    model = bootstraper.fit_population_model()
    cantidad_nidos = pd.DataFrame(nidos_array)
    (
        obtained_first_number,
        obtained_first_number_calculated,
        obtained_last_number,
        obtained_last_number_calculated,
    ) = lam.calculate_interest_numbers(cantidad_nidos, model)

    expected_first_number = "283 (2014)"
    expected_first_number_calculated = "326.1481866290459 (2014)"
    expected_last_number = "{847} (2019)"
    expected_last_number_calculated = "792.2915311946396 (2019)"

    assert obtained_first_number == expected_first_number
    assert obtained_first_number_calculated[0:6] == expected_first_number_calculated[0:6]
    assert obtained_last_number == expected_last_number
    assert obtained_last_number_calculated[0:6] == expected_last_number_calculated[0:6]


def test_generate_season_interval():
    datos_di = {"Temporada": [1, 2, 3, 4, 5], "Maxima_cantidad_nidos": [1, 1, 1, 1, 1]}
    df = pd.DataFrame(datos_di)
    parametrizer = lam.Bootstrap["testing"]
    parametrizer.set_data(df)
    bootstraper = lam.LambdasBootstrapper(parametrizer)
    expected_interval = "(1-5)"
    obtained_interval = bootstraper.generate_season_interval()
    assert expected_interval == obtained_interval


def test_calculate_percent_diff_in_seasons():
    datos_di = {"Maxima_cantidad_nidos": [1, 2, 3, 4, 5]}
    df = pd.DataFrame(datos_di)
    expected_percent = 400
    obtaibed_percent = lam.calculate_percent_diff_in_seasons(df, df["Maxima_cantidad_nidos"])
    assert expected_percent == obtaibed_percent
    datos_d1 = {"Maxima_cantidad_nidos": [0, 2, 3, 4, 5]}
    df_2 = pd.DataFrame(datos_d1)
    expected_percent = 400
    obtaibed_percent = lam.calculate_percent_diff_in_seasons(df_2, df["Maxima_cantidad_nidos"])
    assert expected_percent == obtaibed_percent


testdata = [
    (
        "tests/data/unsorted_seasons.csv",
        "2010-2021",
    ),
    (
        "tests/data/repeated_seasons.csv",
        "2010-2021",
    ),
    (
        "tests/data/one_season.csv",
        "2010",
    ),
]


@pytest.mark.parametrize("path,expected_seasons", testdata)
def test_get_monitored_seasons(path, expected_seasons):
    burrows_data_dataframe = get_df(path)
    parametrizer = lam.Bootstrap["testing"]
    parametrizer.set_data(burrows_data_dataframe)
    bootstraper = lam.LambdasBootstrapper(parametrizer)
    obtained_seasons = bootstraper.get_monitored_seasons()
    assert expected_seasons == obtained_seasons


def test_calculate_growth_rates_table():
    data = pd.read_csv("tests/data/subset_burrows_data.csv")
    bootstrap = lam.Bootstrap["testing"]
    bootstrap.set_data(data)
    tabla = lam.calculate_growth_rates_table(bootstrap)
    p_valor_mayor = tabla[10]
    p_valor_menor = tabla[11]
    expected_p_valor_mayor = 0.0
    expected_p_valor_menor = 1.0
    assert expected_p_valor_mayor == p_valor_mayor
    assert expected_p_valor_menor == p_valor_menor
    obtained_central, obtained_inferior, obtained_superior = tabla[6:9]
    assert obtained_central == 1.18
    assert obtained_superior == "+8.32"
    assert obtained_inferior == "-0.15"
    latex_intervals = tabla[4]
    assert latex_intervals == "1.18 (1.04 - 9.5)"


def test_Bootstrap_from_time_series_parametrizer():
    expected_alpha = 0.067
    parameters = Bootstrap_from_time_series_parametrizer(
        blocks_length=3, N=2000, column_name="Maxima_cantidad_nidos", alpha=expected_alpha
    )
    assert parameters.parameters["alpha"] == expected_alpha


def test_set_axis_plot_config():
    _, ax = gp.geci_plot()
    lam.set_axis_plot_config(ax)
    assert plt.xlim() == (0, 1)
    assert plt.ylim() == (0, 1)
    assert ax.get_xlabel() == "Año"
    assert ax.get_ylabel() == "Cantidad de parejas reproductoras"
    assert ax.get_xticklabels()[0].get_fontsize() == 20
    assert ax.get_yticklabels()[1].get_rotation() == 90.0
