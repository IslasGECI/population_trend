import numpy as np


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
        pass
