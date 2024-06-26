import geci_test_tools as gtt
import pandas as pd
import matplotlib as plt
from population_trend import Population_Trend_Model, Plotter_Population_Trend_Model_From_CPUE

variable_of_interest = "max_CPUE"
assp_cpue_data_for_plotter = pd.DataFrame(
    {variable_of_interest: [1, 1, 2], "Temporada": [2020, 2021, 2020]}
)
pop_model = Population_Trend_Model(
    assp_cpue_data_for_plotter,
    {"intervals": [], "bootstrap_intermediate_distribution": []},
    variable_of_interest,
)


def test_plotter_from_cpue():
    Plotter = Plotter_Population_Trend_Model_From_CPUE(assp_cpue_data_for_plotter, pop_model)
    Plotter.set_labels()
    Plotter.plot_data()
    Plotter.set_legend_location()
    plotter_ax = Plotter.ax
    assert isinstance(plotter_ax, plt.axes._axes.Axes)

    obtained_y_label = plotter_ax.get_ylabel()
    expected_y_label = "CPUE"
    assert obtained_y_label == expected_y_label
    assert plotter_ax.get_yaxis().get_label().get_fontsize() == 20.0

    assert plotter_ax.get_legend().texts[0].get_text() == "Maximum CPUE"

    output_path = "tests/population_trend_from_cpue.png"
    gtt.if_exist_remove(output_path)
    Plotter.savefig(output_path=output_path)
    gtt.assert_exist(output_path)
