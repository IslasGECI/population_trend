import pytest
from unittest.mock import Mock
import pandas as pd
import numpy as np

from population_trend import Population_Trend_Model, Plotter_Population_Trend_Model


@pytest.mark.mpl_image_compare
def tests_Plotter_Population_Trend_Model():
    model = Mock(spec=Population_Trend_Model)
    model.model_med = np.linspace(1, 3, 100)
    dataframe = pd.DataFrame({"Isla": [1, 3], "Temporada": [2020, 2021]})
    Plotter = Plotter_Population_Trend_Model(dataframe)
    Plotter.set_labels()
    return Plotter.plot_model(model)
