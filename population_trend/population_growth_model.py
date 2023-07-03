import numpy as np
from geci_plots import geci_plot, roundup, ticks_positions_array, order_magnitude
from bootstrapping_tools import power_law, lambda_calculator
import matplotlib.pyplot as plt


def normalize_seasons(df):
    first_season = int(df.Temporada.min())
    last_season = int(df.Temporada.max())
    return np.linspace(first_season, last_season, last_season - first_season + 1).astype(int)


def calculate_model_domain(data):
    last_value = data.Temporada.max() - data.Temporada.min()
    return np.linspace(0, last_value, 100)


def calculate_upper_limit(data_interest_variable):
    upper_limit = roundup(
        data_interest_variable.max() * 1.2,
        10 ** order_magnitude(data_interest_variable),
    )
    return upper_limit


class Population_Trend_Model:
    def __init__(self, fit_data, intervals, interest_variable):
        self.intervals = intervals
        self.model_domain = calculate_model_domain(fit_data)
        self.initial_population = lambda_calculator(
            fit_data["Temporada"], fit_data[interest_variable]
        )[1]

    @property
    def model_min(self):
        return power_law(self.model_domain, self.intervals[0], self.initial_population)

    @property
    def model_med(self):
        return power_law(self.model_domain, self.intervals[1], self.initial_population)

    @property
    def model_max(self):
        return power_law(self.model_domain, self.intervals[2], self.initial_population)


class Plotter_Population_Trend_Model:
    def __init__(self, data):
        self.fig, self.ax = geci_plot()
        self.data = data
        self.plot_seasons = self.data["Temporada"][:] - self.data["Temporada"].iloc[0] + 1
        self.ticks_text = normalize_seasons(self.data)
        self.ticks_positions = ticks_positions_array(self.ticks_text)
        self.plot_domain = np.linspace(self.ticks_positions.min(), self.ticks_positions.max(), 100)

    def plot_smooth(self, Population_Trend_Model):
        self.ax.fill_between(
            self.plot_domain,
            Population_Trend_Model.model_min,
            Population_Trend_Model.model_max,
            alpha=0.2,
            label="Confidence zone",
            color="b",
        )

    def plot_model(self, Population_Trend_Model):
        plt.plot(
            self.plot_domain,
            Population_Trend_Model.model_med,
            label="Population growth model",
            color="b",
        )
        return self.fig

    def plot_data(self, variable_to_bootstrap):
        plt.plot(
            self.plot_seasons,
            self.data[variable_to_bootstrap],
            "-Dk",
            label="Active Nests",
        )

    def plot_growth_rate_interval(self, legend_mpl_object, lambda_latex):
        legend_box_positions = legend_mpl_object.get_window_extent()
        self.ax.annotate(
            r"$\lambda =$ {}".format(lambda_latex),
            (legend_box_positions.p0[0], legend_box_positions.p1[1] - 320),
            xycoords="figure pixels",
            fontsize=25,
            color="k",
            alpha=1,
        )

    def set_y_lim(self, fit_data):
        self.ax.set_ylim(
            0,
            calculate_upper_limit(fit_data),
        )

    def set_x_lim(self):
        plt.xlim(
            self.ticks_positions.min() - 0.2,
            self.ticks_positions.max(),
        )

    def set_labels(self):
        plt.ylabel("Number of breeding pairs", size=20)
        plt.xlabel("Seasons", size=20)

    def set_ticks(self):
        plt.xticks(
            self.ticks_positions,
            self.ticks_text,
            rotation=90,
            size=20,
        )
        plt.yticks(size=20)

    def draw(self):
        plt.gcf().subplots_adjust(bottom=0.2)
        plt.draw()

    def savefig(self, islet, output_path=None):
        if output_path is None:
            plt.savefig(
                "reports/figures/cormorant_population_trend_{}".format(
                    islet.replace(" ", "_").lower()
                ),
                dpi=300,
            )
        else:
            plt.savefig(
                output_path,
                dpi=300,
            )

    def set_legend_location(self, islet):
        legend_mpl_object = plt.legend(loc="best")
        if islet == "Natividad":
            legend_mpl_object = plt.legend(loc="upper left")
        return legend_mpl_object
