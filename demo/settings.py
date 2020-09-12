from pathlib import Path
import yaml  # pip install pyyaml


__all__ = ('load_conf', )


def load_conf(config_file=None):
    default_file = Path(__file__).parent / 'config.yaml'
    print(default_file)
    with open(default_file, 'r') as f:
        config = yaml.safe_load(f)

    cf_dict = {}
    if config_file:
        cf_dict = yaml.safe_load(config_file)

    config.update(**cf_dict)

    return config
