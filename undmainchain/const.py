import os
from pathlib import Path

GENESIS = 'https://raw.githubusercontent.com/unification-com/testnet/master' \
          '/latest/genesis.json'

DEFAULT_BUCKET = 'genesis-export'

COMMON = {
    'und': '/usr/local/bin/und',
    'undcli': '/usr/local/bin/undcli',
    'export_bucket': DEFAULT_BUCKET
}

MACHINES = {
    'default': {
        'service': 'und',
        'home': Path(os.path.expanduser("~")) / '.und_mainchain',
        'user': 'root'
    },
    'shark': {
        'service': 'und',
        'home': Path('/home/deploy/.und_mainchain'),
        'user': 'deploy'
    },
    'node1': {
        'service': 'node1',
        'home': Path('/home/deploy/node1/.und_mainchain'),
        'user': 'deploy'
    },
    'node2': {
        'service': 'node2',
        'home': Path('/home/deploy/node2/.und_mainchain'),
        'user': 'deploy'
    },
    'node3': {
        'service': 'node3',
        'home': Path('/home/deploy/node3/.und_mainchain'),
        'user': 'deploy'
    },
    'sentinel1': {
        'service': 'sentinel1',
        'home': Path('/home/deploy/sentinel1/.und_mainchain'),
        'user': 'deploy'
    }
}


def get_defaults():
    d = {}
    for key, value in MACHINES.items():
        d[key] = {**value, **COMMON}
    return d
