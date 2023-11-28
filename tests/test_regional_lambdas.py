import json

laal_path = "tests/data/laal_intervals.json"
with open(laal_path) as json_file:
    laal = json.load(json_file)
