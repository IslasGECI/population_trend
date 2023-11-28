import json
from population_trend import read_distribution

laal_path = "tests/data/laal_intervals.json"
with open(laal_path) as json_file:
    laal = json.load(json_file)


def test_read_distribution():
    distribution = read_distribution(laal)
    obtained_first_element = distribution[0]
    expected_first_element = 1.2130418011696964
    assert obtained_first_element == expected_first_element
    expected_n = 92
    obtained_n = len(distribution)
    assert obtained_n == expected_n
