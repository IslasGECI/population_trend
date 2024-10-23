from population_trend import Plotter_Growth_Rate
import pytest
import matplotlib as plt
import numpy as np


def test_plotter_growth_rate():
    lambdas_california = {"intervals": [1, 2, 3.5]}
    lambdas_pacific = {"intervals": [1.9, 3, 7.5]}
    regional_names = ["Gulf of California", "Pacific"]
    plotter = Plotter_Growth_Rate(lambdas_california, lambdas_pacific, regional_names)
    obtained = plotter.plot_error_bars()
    assert isinstance(obtained, plt.axes._axes.Axes)

    x_positions = plotter.error_bar_container.lines[0].get_data()[0]
    y_positions = plotter.error_bar_container.lines[0].get_data()[1]
    np.testing.assert_array_equal(x_positions, [1, 2])
    np.testing.assert_array_equal(y_positions, [2, 3])

    obtained_segments = plotter.error_bar_container.lines[2][0].properties()["segments"]
    assert obtained_segments[0][0][1] == lambdas_california["intervals"][0]
    assert obtained_segments[0][1][1] == lambdas_california["intervals"][2]
    assert obtained_segments[1][0][1] == lambdas_pacific["intervals"][0]
    assert obtained_segments[1][1][1] == lambdas_pacific["intervals"][2]

    obtained_y_label = obtained.get_ylabel()
    expected_y_label = "Growth Rate"
    assert obtained_y_label == expected_y_label
    assert obtained.get_xticklabels()[0].get_text() == "Gulf of California"
    assert obtained.get_xticklabels()[1].get_text() == "Pacific"
    assert obtained.get_xticklabels()[1].get_fontsize() == 20.0

    obtained_xlim = plt.pyplot.xlim()
    expected_xlim = (0.5, 2.5)
    assert obtained_xlim == expected_xlim

    obtained_h_line_in_1 = plotter.horizontal_line
    segment = obtained_h_line_in_1.properties()["segments"][0]
    height = 1
    assert segment[0][1] == height
    assert segment[1][1] == height

    linestyle = obtained_h_line_in_1.get_linestyle()[0][1]
    assert pytest.approx(linestyle) == [5.55, 2.4]

    color_line = obtained_h_line_in_1.get_color()[0]
    np.testing.assert_almost_equal(color_line, [0, 0.5019607, 0, 1])
