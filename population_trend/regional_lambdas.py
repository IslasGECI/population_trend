def read_distribution(json_dict):
    completed_distribution = json_dict["bootstrap_intermediate_distribution"]
    lambdas_distribution = [sample[0] for sample in completed_distribution]
    return lambdas_distribution
