def read_distribution(json_dict):
    completed_distribution = json_dict["bootstrap_intermediate_distribution"]
    return completed_distribution[0]
