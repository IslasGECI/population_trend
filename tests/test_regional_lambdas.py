import os
import numpy as np
from population_trend import (
    Calculator_Regional_Lambdas_Intervals,
    Island_Bootstrap_Distribution_Concatenator,
)

config_path = "tests/data/region_config.json"


def test_Island_Bootstrap_Distribution_Concatenator():
    concatenator = Island_Bootstrap_Distribution_Concatenator(config_path)
    concatenator.set_region("region_1")

    expected_number_distributions = 2
    obtained_number_of_distributions = len(concatenator.distributions)
    assert obtained_number_of_distributions == expected_number_distributions

    expected_len_laal_distribution = 92
    obtained_len_laal_distribution = len(concatenator.distributions[0])
    assert obtained_len_laal_distribution == expected_len_laal_distribution

    obtained_first_element = concatenator.distributions[0][0]
    expected_first_element = 1.2130418011696964
    assert obtained_first_element == expected_first_element

    expected_len_gumu_distribution = 1892
    obtained_len_gumu_distribution = len(concatenator.distributions[1])
    assert obtained_len_gumu_distribution == expected_len_gumu_distribution

    obtained_mean_distribution = concatenator.mean_by_row()
    expected_mean_distribution_length = 2000
    assert len(obtained_mean_distribution) == expected_mean_distribution_length
    assert obtained_mean_distribution[0] == 1.3687478379206273
    assert obtained_mean_distribution[1] == 1.40338597444926


def test_Calculator_Regional_Lambdas_Intervals():
    regional_lambdas = np.array([0.1, 0.2, 0.3, 2.0, 2.0, 2.0, 4.0])
    calculator = Calculator_Regional_Lambdas_Intervals(regional_lambdas)
    obtained = calculator.lambdas
    assert (obtained == regional_lambdas).all()
    output_path = "tests/regional_intervals.json"
    calculator.save_intervals(output_path)
    assert os.path.exists(output_path)
    p_values = calculator.p_values
    expected = (3 / 7, 4 / 7)
    assert p_values == expected, "It obtains the right p-values"

    obtained_intervals = calculator.intervals
    expected_intervals = [0.1, 2.0, 4.0]
    assert obtained_intervals == expected_intervals

    obtained_intervals = calculator.lambda_latex_interval
    expected_intervals = "2.0 (0.1 - 4.0)"
    assert obtained_intervals == expected_intervals
