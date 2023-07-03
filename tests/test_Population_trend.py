from population_trend import (
    calculate_model_domain,
    calculate_upper_limit,
    filter_data_by_islet,
    normalize_seasons,
    Plotter_Population_Trend_Model,
    Population_Trend_Model,
)
from geci_plots import geci_plot
import os
import pandas as pd
import numpy as np
from pandas._testing import assert_frame_equal


cormorant_data = pd.DataFrame({"Isla": ["a", "a", "b"], "Temporada": [2020, 2021, 2020]})
expected_data = pd.DataFrame({"Isla": ["a", "a"], "Temporada": [2020, 2021]})


def test_filter_data_by_islet():
    obtained_data = filter_data_by_islet(cormorant_data, "a")
    assert_frame_equal(expected_data, obtained_data)


def test_normalize_seasons():
    expected_date = np.array([2020, 2021])
    obtained_date = normalize_seasons(cormorant_data)
    np.testing.assert_array_equal(expected_date, obtained_date)


def test_calculate_model_domain():
    obtained = calculate_model_domain(cormorant_data)
    obtained_length = len(obtained)
    expected_length = 100
    assert obtained_length == expected_length

    obtained_t0 = obtained[0]
    expected_t0 = 0
    assert obtained_t0 == expected_t0

    obtained_t0 = obtained[-1]
    expected_t0 = 1
    assert obtained_t0 == expected_t0


def tests_calculate_upper_limit():
    expected_limit = calculate_upper_limit(cormorant_data["Temporada"])
    obtained_limit = 3000
    assert expected_limit == obtained_limit


Plotter = Plotter_Population_Trend_Model(cormorant_data)


class Tests_Plotter_Population_Trend_Model:
    def tests_init_(self):
        fig, ax = geci_plot()
        assert type(fig) == type(Plotter.fig)  # noqa
        assert Plotter.data is not None

    def tests_time_to_model(self):
        obtained = Plotter.time_to_model
        expected_first_point = 1
        assert obtained[0] == expected_first_point
        expected_last_point = 2.05
        assert obtained[-1] == expected_last_point

    def tests_savefig(self):
        islet = "morro"
        default_path = f"reports/figures/cormorant_population_trend_{islet}.png"
        default_folder = "reports/figures/"
        if not os.path.exists(default_folder):
            os.makedirs(default_folder)
        if os.path.exists(default_path):
            os.remove(default_path)
        Plotter.savefig(islet)
        assert os.path.exists(default_path)
        output_path = "tests/data/prueba.png"
        if os.path.exists(output_path):
            os.remove(output_path)
        Plotter.savefig(islet, output_path)
        assert os.path.exists(output_path)
