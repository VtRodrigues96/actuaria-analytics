import yaml
from pathlib import Path


CONFIG_PATH = (
    Path(__file__)
    .parents[2]
    / "config"
    / "config.yaml"
)


def load_config():

    with open(CONFIG_PATH, "r") as file:
        return yaml.safe_load(file)


config = load_config()