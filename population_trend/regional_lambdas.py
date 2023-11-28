import json
import numpy as np

from bootstrapping_tools import calculate_p_values


def read_distribution(json_dict):
    completed_distribution = json_dict["bootstrap_intermediate_distribution"]
    lambdas_distribution = [sample[0] for sample in completed_distribution]
    return lambdas_distribution


def concatenate_distribution(*argv):
    rng = np.random.default_rng()
    list_of_distributions = []
    for arg in argv:
        resampled = rng.choice(arg, size=2000, replace=True)
        list_of_distributions.append(resampled)
    return np.array(list_of_distributions).T


def mean_by_row(concatenated_distributions):
    return np.mean(concatenated_distributions, axis=1)


class Calculator_Regional_Lambdas:
    def __init__(self, regional_lambdas):
        self.regional_distribution = regional_lambdas
        self.intervals = [1, 2, 3]
        self.interval_lambdas = [1, 3, 7]
        self.p_values = self.get_p_values()

    def get_p_values(self):
        p_value_mayor, p_value_menor = calculate_p_values(self.regional_distribution)
        p_values = (p_value_mayor, p_value_menor)
        return p_values

    def save_intervals(self, output_path):
        json_dict = {
            "intervals": list(self.intervals),
            "lambda_latex_interval": "3 (1 - 7)",
            "p-values": "(0,1)",
            "bootstrap_intermediate_distribution": list(self.regional_distribution),
        }
        with open(output_path, "w") as file:
            json.dump(json_dict, file)
