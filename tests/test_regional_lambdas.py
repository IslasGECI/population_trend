import json
from population_trend import read_distribution

laal_path = "tests/data/laal_intervals.json"
with open(laal_path) as json_file:
    laal = json.load(json_file)


def test_read_distribution():
    distribution = read_distribution(laal)
