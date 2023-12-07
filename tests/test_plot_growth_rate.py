from population_trend import Plotter_Growth_Rate
import matplotlib as plt


def test_plotter_growth_rate():
    lambdas_dict = {"intervals": [1, 2, 3]}
    plotter = Plotter_Growth_Rate(lambdas_dict, lambdas_dict)
    obtained = plotter.plot_error_bars()
    assert plotter.interval == [[1, 2, 3], [1, 2, 3]]
    assert isinstance(obtained, plt.axes._axes.Axes)
