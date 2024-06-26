import hashlib
import pytest
from unittest.mock import Mock
import pandas as pd
import numpy as np
import os

from population_trend import (
    Population_Trend_Model,
    Plotter_Population_Trend_Model,
    plot_population_trend,
)

intervals_path = "tests/data/gumu_guadalupe_boostrap_intervals.json"


def test_plot_population_trend():
    data_path = "tests/data/gumu_guadalupe_data.csv"
    output_path = "tests/data/gumu_guadalupe_population_trend.png"
    if os.path.exists(output_path):
        os.remove(output_path)
    plot_population_trend(
        data_path=data_path, intervals_path=intervals_path, output_path=output_path
    )
    assert os.path.exists(output_path)
    obtained_hash = hashlib.md5(open(output_path, "rb").read()).hexdigest()
    expected_hash = "0526f34add8c1091b19c65ed33cfe612"

    assert obtained_hash == expected_hash


@pytest.mark.mpl_image_compare
def tests_Plotter_Population_Trend_Model():
    model = Mock(spec=Population_Trend_Model)
    model.med_model = np.linspace(1, 3, 100)
    model.interest_variable = "Maxima_cantidad_nidos"
    dataframe = pd.DataFrame({"Isla": [1, 3], "Temporada": [2020, 2021]})
    Plotter = Plotter_Population_Trend_Model(dataframe, model)
    Plotter.set_labels()
    return Plotter.plot_model()
