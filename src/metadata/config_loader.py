from pathlib import Path
import yaml


def load_config(config_path: str) -> dict:

    config_file = Path(config_path)

    if not config_file.exists():
        raise FileNotFoundError(
            f"Config file not found: {config_path}"
        )

    with open(config_file, "r") as file:
        config = yaml.safe_load(file)

    if config is None:
        raise ValueError(
            f"Empty or invalid YAML file: {config_path}"
        )

    return config