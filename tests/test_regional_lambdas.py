import os
import json
import numpy as np
from population_trend import (
    read_distribution,
    concatenate_distribution,
    mean_by_row,
    Calculator_Regional_Lambdas,
)

laal_path = "tests/data/laal_intervals_for_tests.json"
with open(laal_path) as json_file:
    laal = json.load(json_file)

gumu_path = "tests/data/gumu_guadalupe_boostrap_intervals.json"
with open(gumu_path) as json_file:
    gumu = json.load(json_file)


def test_read_distribution():
    distribution = read_distribution(laal)
    obtained_first_element = distribution[0]
    expected_first_element = 1.2130418011696964
    assert obtained_first_element == expected_first_element
    expected_n = 92
    obtained_n = len(distribution)
    assert obtained_n == expected_n

    distribution = read_distribution(gumu)
    expected_n = 1892
    obtained_n = len(distribution)
    assert obtained_n == expected_n


def test_concatenate_distribution():
    laal_distribution = [1, 1, 1, 1]
    gumu_distribution = [2, 2, 2, 2]
    expected_shape = (2000, 2)
    concatenated = concatenate_distribution(laal_distribution, gumu_distribution)
    obtained_shape = np.shape(concatenated)
    assert obtained_shape == expected_shape

    expected_shape = (2000, 3)
    concatenated = concatenate_distribution(laal_distribution, gumu_distribution, laal_distribution)
    obtained_shape = np.shape(concatenated)
    assert obtained_shape == expected_shape


def test_mean_by_row():
    concatenated = np.array([[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]]).T
    obtained = mean_by_row(concatenated)
    expected = np.array([2, 2, 2, 2])
    assert (obtained == expected).all()


def test_Calculator_Regional_Lambdas():
    regional_lambdas = np.array([0.1, 0.2, 0.3, 2.0, 2.0, 2.0, 4.0])
    calculator = Calculator_Regional_Lambdas(regional_lambdas)
    obtained = calculator.regional_distribution
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
