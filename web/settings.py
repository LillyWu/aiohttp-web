import argparse
import trafaret as T
from trafaret_config import commandline
import pathlib

TRAFARET = T.Dict({
    T.Key('port'): T.Int(),
    T.Key('host'): T.IP,
    T.Key('mysql'):
        T.Dict({
            'db': T.String(),
            'user': T.String(),
            'password': T.String(),
            'host': T.String(),
            'port': T.Int(),
        }),
})

BASE_DIR = pathlib.Path(__file__).parent.parent
DEFAULT_CONFIG_PATH = BASE_DIR / 'config' / 'web.yaml'

def get_config(argv=None):
    ap = argparse.ArgumentParser()
    commandline.standard_argparse_options(ap, default_config=DEFAULT_CONFIG_PATH)

    options = ap.parse_args()
    config = commandline.config_from_options(options, TRAFARET)
    return config
