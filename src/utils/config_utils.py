import yaml

CONFIG_PATH = "./config/categories.yaml"


def load_categories_for_industry(industry: str):
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)

    return config.get(industry, [])


def get_supported_industries():
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)
    return list(config.keys())
