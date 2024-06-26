from population_trend.population_growth_model import Plotter_Population_Trend_Model

import matplotlib.pyplot as plt


class Plotter_Population_Trend_Model_From_CPUE(Plotter_Population_Trend_Model):
    def set_labels(self):
        plt.ylabel("CPUE", size=20)
        plt.xlabel("Seasons", size=20)

    def plot_data(self):
        plt.plot(
            self.plot_seasons,
            self.data[self.interest_variable],
            "-Dk",
            label="Maximum CPUE",
        )

    def set_legend_location(
        self,
    ):
        legend_mpl_object = plt.legend(loc="best")
        return legend_mpl_object

    def savefig(self, output_path):
        self.set_x_lim()
        self.set_y_lim()
        self.set_labels()
        self.set_ticks()
        self.draw()
        transparent_background = True
        plt.savefig(output_path, dpi=300, transparent=transparent_background)
