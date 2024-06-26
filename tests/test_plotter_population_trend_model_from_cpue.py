import pandas as pd
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
Plotter = Plotter_Population_Trend_Model_From_CPUE(assp_cpue_data_for_plotter, pop_model)
