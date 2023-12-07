from population_trend import Plotter_Growth_Rate
import matplotlib as plt


def test_plotter_growth_rate():
    lambdas_dict = {"intervals": [1, 2, 3]}
    lambdas_dict_2 = {"intervals": [2, 3, 8]}
    plotter = Plotter_Growth_Rate(lambdas_dict, lambdas_dict_2)
    obtained = plotter.plot_error_bars()
    assert plotter.interval == [[1, 2, 3], [2, 3, 8]]
    assert isinstance(obtained, plt.axes._axes.Axes)
    obtained_y_label = obtained.get_ylabel()
    expected_y_label = "Growth Rate"
    assert obtained_y_label == expected_y_label
    plt.pyplot.savefig("tests/data/borrame.png")
    assert obtained.get_xticklabels()[0].get_text() == "California"
    assert obtained.get_xticklabels()[1].get_text() == "Pacific"
    assert obtained.get_xticklabels()[1].get_fontsize() == 20.0

    obtained_xlim = plt.pyplot.xlim()
    expected_xlim = (0.5, 2.5)
    assert obtained_xlim == expected_xlim
