import numpy as np


def read_distribution(json_dict):
    completed_distribution = json_dict["bootstrap_intermediate_distribution"]
    lambdas_distribution = [sample[0] for sample in completed_distribution]
    return lambdas_distribution


def concatenate_distribution(distribution_1, distribution_2):
    rng = np.random.default_rng()
    completed_1 = rng.choice(distribution_1, size=2000, replace=True)
    completed_2 = rng.choice(distribution_2, size=2000, replace=True)
    return np.array([completed_1, completed_2]).T
