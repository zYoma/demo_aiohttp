import os
from pathlib import Path

import yaml  # pip install pyyaml


__all__ = ('load_conf')

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = os.path.join(BASE_DIR, 'static')

DEBUG = True
REDIS_CON = 'localhost', 6379

DATABASE = {
    'database': 'demo_aiohttp',
    'password': 'kdfs&923lf',
    'user': 'aiohttp_user',
    'host': 'localhost',
}


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
