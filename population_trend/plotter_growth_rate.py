import geci_plots as gp


class Plotter_Growth_Rate:
    def __init__(self, lambdas_dict, lambdas_dict_2):
        self.interval = [lambdas_dict["intervals"], lambdas_dict_2["intervals"]]

    def plot_error_bars(self):
        _, ax = gp.geci_plot()
        return ax
