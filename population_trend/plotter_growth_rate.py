import geci_plots as gp
import matplotlib.pyplot as plt


class Plotter_Growth_Rate:
    def __init__(self, lambdas_dict, lambdas_dict_2):
        self.interval = [lambdas_dict["intervals"], lambdas_dict_2["intervals"]]

    def plot_error_bars(self):
        _, ax = gp.geci_plot()
        low_limits = [
            self.interval[0][1] - self.interval[0][0],
            self.interval[1][1] - self.interval[1][0],
        ]
        up_limits = [
            self.interval[0][2] - self.interval[0][1],
            self.interval[1][2] - self.interval[1][1],
        ]
        yerror = [low_limits, up_limits]
        xticks_position = [1, 2]
        self.error_bar_container = plt.errorbar(
            xticks_position,
            [self.interval[0][1], self.interval[1][1]],
            yerr=yerror,
            fmt="o",
        )
        plt.ylabel("Growth Rate", fontsize=20)
        plt.xticks(xticks_position, ["California", "Pacific"], fontsize=20)
        plt.xlim([0.5, 2.5])
        return ax
