import json
import numpy as np
from population_trend import (
    read_distribution,
    concatenate_distribution,
    mean_by_row,
    Calculator_Regional_Lambdas,
)

laal_path = "tests/data/laal_intervals.json"
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
    regional_lambdas = np.array([2, 2, 2, 2, 2, 2])
    Calculator_Regional_Lambdas()
