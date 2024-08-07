import yaml


def load_config(file_path) -> dict:
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


configs = {
    "INITIAL_CASH": 1000,
    "liq_pool_limit": 10,
    "timeSpan": 60,
    "DATABASE_NAME": 'sharktank',
}