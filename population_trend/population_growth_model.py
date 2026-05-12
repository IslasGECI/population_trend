import numpy as np
from geci_plots import geci_plot, roundup, ticks_positions_array, order_magnitude
from bootstrapping_tools import power_law, lambda_calculator
import matplotlib.pyplot as plt


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
    def __init__(self, fit_data, json_parameters, interest_variable):
        self.intervals = json_parameters["intervals"]
        self.model_domain = calculate_model_domain(fit_data)
        self.interest_variable = interest_variable
        self.initial_population = lambda_calculator(
            fit_data["Temporada"], fit_data[self.interest_variable]
        )
        self.bootstrap_distribution = json_parameters["bootstrap_intermediate_distribution"]

    def intern_model(self, i):
        return power_law(
            self.model_domain, self.bootstrap_distribution[i][0], self.bootstrap_distribution[i][1]
        )

    @property
    def min_model(self):
        return power_law(self.model_domain, self.intervals[0][0], self.intervals[0][1])

    @property
    def med_model(self):
        return power_law(self.model_domain, self.intervals[1][0], self.intervals[1][1])

    @property
    def max_model(self):
        return power_law(self.model_domain, self.intervals[2][0], self.intervals[2][1])


class Plotter_Population_Trend_Model:
    def __init__(self, data, population_model, tick_mode, language="english"):
        self.fig, self.ax = geci_plot()
        self.ax.legend()
        self.fill_missing_seasons(data)
        self.tick_mode = tick_mode
        self.language = language
        self.seasons_to_plot = self.filled_data.index.values + 1
        self.ticks_positions = ticks_positions_array(self.filled_data)
        self.domain_plot = np.linspace(self.ticks_positions.min(), self.ticks_positions.max(), 100)
        self.population_model = population_model
        self.interest_variable = population_model.interest_variable

    def fill_missing_seasons(self, data):
        self.data = data
        self.data.Temporada = self.data.Temporada.astype(int)
        self.data = self.data.set_index("Temporada")
        full_seasons = range((self.data.index.min()), self.data.index.max() + 1)
        self.filled_data = (
            self.data.reindex(full_seasons).reset_index().rename(columns={"index": "Temporada"})
        )

    def plot_smooth(self):
        self.ax.fill_between(
            self.domain_plot,
            self.population_model.min_model,
            self.population_model.med_model,
            label="Confidence zone",
            color="powderblue",
        )
        self.ax.fill_between(
            self.domain_plot,
            self.population_model.med_model,
            self.population_model.max_model,
            color="powderblue",
        )
        self.ax.fill_between(
            self.domain_plot,
            self.population_model.min_model,
            self.population_model.max_model,
            color="powderblue",
        )
        number_of_samples = len(self.population_model.bootstrap_distribution)
        for i in range(0, number_of_samples - 1, 10):
            self.ax.fill_between(
                self.domain_plot,
                self.population_model.intern_model(i),
                self.population_model.med_model,
                color="powderblue",
            )
            self.ax.fill_between(
                self.domain_plot,
                self.population_model.intern_model(i),
                self.population_model.intern_model(i + 1),
                color="powderblue",
            )
        self.ax.fill_between(
            self.domain_plot,
            self.population_model.intern_model(i + 1),
            self.population_model.med_model,
            color="powderblue",
        )

    def plot_model(self):
        plt.plot(
            self.domain_plot,
            self.population_model.med_model,
            label="Population growth model",
            color="b",
        )
        return self.fig

    def plot_data(self):
        self.ax.plot(
            self.seasons_to_plot,
            self.filled_data[self.interest_variable],
            "-Dk",
            label="Active Nests",
        )

    def show_legend(self, show_legend):
        if not show_legend:
            self.ax.get_legend().remove()

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

    def set_y_lim(self):
        self.ax.set_ylim(
            0,
            calculate_upper_limit(self.data[self.interest_variable]),
        )

    def set_x_lim(self):
        plt.xlim(
            self.ticks_positions.min() - 0.2,
            self.ticks_positions.max(),
        )

    def set_labels(self):
        labels = {
            "english": {"ylabel": "Number of breeding pairs", "xlabel": "Seasons"},
            "spanish": {"ylabel": "Número de parejas reproductivas", "xlabel": "Temporadas"},
        }
        self.ax.set_ylabel(labels[self.language]["ylabel"], size=20)
        self.ax.set_xlabel(labels[self.language]["xlabel"], size=20)

    def set_ticks(self):
        self.get_tick_step()
        self.ticks_text = self.filled_data.Temporada.values.astype(int)
        plt.xticks(
            self.ticks_positions[:: self.tick_step],
            self.ticks_text[:: self.tick_step],
            rotation=90,
            size=20,
        )
        plt.yticks(size=20)

    def get_tick_step(self):
        tick_modes = {"sparse": 2, "full": 1}
        self.tick_step = tick_modes[self.tick_mode]

    def draw(self):
        plt.gcf().subplots_adjust(bottom=0.2)
        plt.draw()

    def savefig(self, islet, output_path=None):
        self.set_x_lim()
        self.set_y_lim()
        self.set_labels()
        self.set_ticks()
        self.draw()
        transparent_background = True
        if output_path is None:
            output_path = "reports/figures/cormorant_population_trend_{}".format(
                islet.replace(" ", "_").lower()
            )
        plt.savefig(output_path, dpi=300, transparent=transparent_background)

    def set_legend_location(self, islet):
        legend_mpl_object = plt.legend(loc="best")
        if islet == "Natividad":
            legend_mpl_object = plt.legend(loc="upper left")
        return legend_mpl_object
