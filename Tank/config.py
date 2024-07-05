import yaml


def load_config(file_path) -> dict:
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


configs = {
    "investment": 1000,
    "liq_pool_limit": 10,
    "DATABASE_NAME": 'sharktank',
    "fees": 0.0,
}