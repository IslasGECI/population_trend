import json
import pandas as pd
from population_trend.plot_population_trend import _plot_population_trend

fit_data = pd.read_csv("tests/data/gumu_guadalupe_data.csv")
intervals_path = "tests/data/gumu_guadalupe_boostrap_intervals.json"
with open(intervals_path, "r") as read_file:
    intervals_json = json.load(read_file)


class TestPlotPopulationTrendShowLegend:
    """Tests for the show_legend parameter of _plot_population_trend."""

    def test_show_legend_true_keeps_legend(self):
        """When show_legend=True (default), legend should be present on the axes."""
        graficador = _plot_population_trend(
            fit_data,
            intervals_json,
            show_legend=True,
        )
        assert graficador.ax.get_legend() is not None

    def test_show_legend_false_hides_legend(self):
        """When show_legend=False, legend should be removed from the axes."""
        graficador = _plot_population_trend(
            fit_data,
            intervals_json,
            show_legend=False,
        )
        assert graficador.ax.get_legend() is None


class TestPlotPopulationTrendLabelLanguage:
    """Tests for the language parameter of _plot_population_trend."""

    def test_label_language_english(self):
        """When language="english", labels should be on english."""
        graficador = _plot_population_trend(
            fit_data,
            intervals_json,
            True,
            language="english",
        )
        graficador.set_labels()
        obtained_labels = [graficador.ax.get_xlabel(), graficador.ax.get_ylabel()]
        expected_labels = ["Seasons", "Number of breeding pairs"]
        assert obtained_labels == expected_labels

    def test_label_language_spanish(self):
        """When language="spanish", labels should be on spanish."""
        graficador = _plot_population_trend(
            fit_data,
            intervals_json,
            True,
            language="spanish",
        )
        graficador.set_labels()
        obtained_labels = [graficador.ax.get_xlabel(), graficador.ax.get_ylabel()]
        expected_labels = ["Temporadas", "Número de parejas reproductivas"]
        assert obtained_labels == expected_labels
