import os
import numpy as np
from population_trend import (
    Calculator_Regional_Lambdas_Intervals,
    Island_Bootstrap_Distribution_Concatenator,
)
import json

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
    alpha = 0.05
    calculator = Calculator_Regional_Lambdas_Intervals(regional_lambdas, alpha)
    obtained = calculator.lambdas
    assert (obtained == regional_lambdas).all()
    output_path = "tests/regional_intervals.json"
    calculator.save_intervals(output_path)
    assert os.path.exists(output_path)

    with open(output_path, encoding="utf8") as json_file:
        json_data = json.load(json_file)

    p_values = calculator.p_values
    expected = (3 / 7, 4 / 7)
    assert p_values == expected, "It obtains the right p-values"

    obtained_intervals = calculator.intervals
    expected_intervals = [0.1, 2.0, 4.0]
    assert obtained_intervals == expected_intervals
    assert json_data["intervals"] == expected_intervals

    obtained_intervals = calculator.lambda_latex_interval
    expected_intervals = "2.0 (0.1 - 4.0)"
    assert obtained_intervals == expected_intervals

    obtained_statement_latex = calculator.hypothesis_test_statement_latex
    expected_statement_latex = "No podemos concluir si la población está creciendo o decreciendo. El valor $p$ calculado resultó mayor que $\\alpha =$ 0.05 para ambas hipótesis nulas. Para $\\lambda>1: p =$ 0.571; para $\\lambda<1: p =$ 0.429"
    assert obtained_statement_latex == expected_statement_latex

    obtained_english_statement_latex = calculator.hypothesis_test_statement_latex_en
    expected_english_statement_latex = "We can not conclude if the population is increasing or decreasing. The calculated $p$-value is higher than the $\\alpha =$ 0.05 for both null hypothesis tests. For $\\lambda>1: p =$ 0.571; for $\\lambda<1: p =$ 0.429"
    assert obtained_english_statement_latex == expected_english_statement_latex
    assert json_data["hypothesis_test_statement_latex_sp"] == expected_statement_latex
    assert json_data["hypothesis_test_statement_latex_en"] == expected_english_statement_latex


def test_Calculator_Regional_Lambdas_Intervals_hypothesis_test_statement_latex():
    decreasing_regional_lambdas = np.array([0.1, 0.2, 0.3, 0.2, 0.2, 0.2, 0.4])
    obtained_statement_latex = obtain_statement_latex(decreasing_regional_lambdas)
    expected_statement_latex = "La población está decreciendo, $\\lambda$ CI 0.2 (0.1 - 0.4) con una significancia $p =$ 0.0"
    assert obtained_statement_latex == expected_statement_latex

    obtained_english_statement_latex = obtain_statement_latex_en(decreasing_regional_lambdas)
    expected_english_statement_latex = (
        "The population is decreasing, $\\lambda$ CI 0.2 (0.1 - 0.4) with a significance $p =$ 0.0"
    )
    assert obtained_english_statement_latex == expected_english_statement_latex

    increasing_regional_lambdas = np.array([1, 2, 3, 2, 2, 2, 4])
    obtained_statement_latex = obtain_statement_latex(increasing_regional_lambdas)
    expected_statement_latex = (
        "La población está creciendo, $\\lambda$ CI 2 (1 - 4) con una significancia $p =$ 0.0"
    )
    assert obtained_statement_latex == expected_statement_latex

    obtained_english_statement_latex = obtain_statement_latex_en(increasing_regional_lambdas)
    expected_english_statement_latex = (
        "The population is increasing, $\\lambda$ CI 2 (1 - 4) with a significance $p =$ 0.0"
    )
    assert obtained_english_statement_latex == expected_english_statement_latex

    increasing_regional_lambdas = np.array(
        [0.4, 8, 2, 3, 2, 2, 2, 4, 3, 5, 7, 1, 2, 3, 2, 2, 2, 4, 3, 5, 7]
    )
    obtained_statement_latex = obtain_statement_latex(increasing_regional_lambdas)
    expected_statement_latex = "La población está creciendo, $\\lambda$ CI 3.0 (1.0 - 8.0) con una significancia $p =$ 0.048"
    assert obtained_statement_latex == expected_statement_latex

    decreasing_regional_lambdas = np.array(
        [
            4,
            0.2,
            0.3,
            0.2,
            0.2,
            0.2,
            0.4,
            0.1,
            0.3,
            0.2,
            0.3,
            0.2,
            0.2,
            0.2,
            0.4,
            0.1,
            0.2,
            0.3,
            0.2,
            0.2,
            0.2,
            0.4,
        ]
    )
    obtained_statement_latex = obtain_statement_latex(decreasing_regional_lambdas)
    expected_statement_latex = "La población está decreciendo, $\\lambda$ CI 0.2 (0.1 - 0.4) con una significancia $p =$ 0.045"
    assert obtained_statement_latex == expected_statement_latex


def obtain_statement_latex(regional_lambdas):
    alpha = 0.05
    calculator = Calculator_Regional_Lambdas_Intervals(regional_lambdas, alpha)
    obtained_statement_latex = calculator.hypothesis_test_statement_latex
    return obtained_statement_latex


def obtain_statement_latex_en(regional_lambdas):
    alpha = 0.05
    calculator = Calculator_Regional_Lambdas_Intervals(regional_lambdas, alpha)
    obtained_statement_latex = calculator.hypothesis_test_statement_latex_en
    return obtained_statement_latex
