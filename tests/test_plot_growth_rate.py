from population_trend import Plotter_Growth_Rate


def test_plotter_growth_rate():
    lambdas_dict = {"intervals": [1, 2, 3]}
    plotter = Plotter_Growth_Rate(lambdas_dict)
