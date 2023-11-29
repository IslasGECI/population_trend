import json
import numpy as np

from bootstrapping_tools import (
    calculate_p_values,
    calculate_intervals_from_p_values_and_alpha,
    generate_latex_interval_string,
)

from population_trend import Bootstrap_from_time_series


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


class Calculator_Regional_Lambdas(Bootstrap_from_time_series):
    def __init__(self, regional_lambdas):
        self.lambdas = regional_lambdas
        self.p_values = self.get_p_values()
        self.intervals = self.intervals_from_p_values_and_alpha()
        self.interval_lambdas = [interval for interval in self.intervals]
        self.lambda_latex_interval = self.get_lambda_interval_latex_string()

    def intervals_from_p_values_and_alpha(self):
        intervals = calculate_intervals_from_p_values_and_alpha(self.lambdas, self.p_values, 0.05)
        return intervals

    def get_intermediate_lambdas(self):
        return [
            lambda_n0
            for lambda_n0 in self.lambdas
            if (lambda_n0 > self.intervals[0]) and (lambda_n0 < self.intervals[2])
        ]

    def save_intervals(self, output_path):
        json_dict = {
            "intervals": list(self.intervals),
            "lambda_latex_interval": self.lambda_latex_interval,
            "p-values": self.p_values,
            "bootstrap_intermediate_distribution": self.get_intermediate_lambdas(),
        }
        with open(output_path, "w") as file:
            json.dump(json_dict, file)
