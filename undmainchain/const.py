import os
from pathlib import Path

GENESIS = 'https://raw.githubusercontent.com/unification-com/mainnet/master' \
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
    'node4': {
        'service': 'node4',
        'home': Path('/home/deploy/node4/.und_mainchain'),
        'user': 'deploy'
    },
    'node5': {
        'service': 'node5',
        'home': Path('/home/deploy/node5/.und_mainchain'),
        'user': 'deploy'
    },
    'node6': {
        'service': 'node6',
        'home': Path('/home/deploy/node6/.und_mainchain'),
        'user': 'deploy'
    },
    'node7': {
        'service': 'node7',
        'home': Path('/home/deploy/node7/.und_mainchain'),
        'user': 'deploy'
    'node8': {
        'service': 'node8',
        'home': Path('/home/deploy/node8/.und_mainchain'),
        'user': 'deploy'
    },
    'node9': {
        'service': 'node9',
        'home': Path('/home/deploy/node9/.und_mainchain'),
        'user': 'deploy'
    },
    'node10': {
        'service': 'node10',
        'home': Path('/home/deploy/node10/.und_mainchain'),
        'user': 'deploy'
    },
    'node11': {
        'service': 'node11',
        'home': Path('/home/deploy/node11/.und_mainchain'),
        'user': 'deploy'
    'node12': {
        'service': 'node12',
        'home': Path('/home/deploy/node12/.und_mainchain'),
        'user': 'deploy'
    },
    'seed1': {
        'service': 'seed1',
        'home': Path('/home/deploy/seed1/.und_mainchain'),
        'user': 'deploy'
    },
    'sentinel1': {
        'service': 'sentinel1',
        'home': Path('/home/deploy/sentinel1/.und_mainchain'),
        'user': 'deploy'
    },
    'sentinel2': {
        'service': 'sentinel2',
        'home': Path('/home/deploy/sentinel2/.und_mainchain'),
        'user': 'deploy'
    },
    'sentinel3': {
        'service': 'sentinel3',
        'home': Path('/home/deploy/sentinel3/.und_mainchain'),
        'user': 'deploy'
    },
    'sentinel4': {
        'service': 'sentinel4',
        'home': Path('/home/deploy/sentinel4/.und_mainchain'),
        'user': 'deploy'
    },
    'sentinel5': {
        'service': 'sentinel5',
        'home': Path('/home/deploy/sentinel5/.und_mainchain'),
        'user': 'deploy'
    },
    'sentinel6': {
        'service': 'sentinel6',
        'home': Path('/home/deploy/sentinel6/.und_mainchain'),
        'user': 'deploy'
    },
    'sentinel7': {
        'service': 'sentinel7',
        'home': Path('/home/deploy/sentinel7/.und_mainchain'),
        'user': 'deploy'
    },
    'sentinel8': {
        'service': 'sentinel8',
        'home': Path('/home/deploy/sentinel8/.und_mainchain'),
        'user': 'deploy'
    },
    'sentinel9': {
        'service': 'sentinel9',
        'home': Path('/home/deploy/sentinel9/.und_mainchain'),
        'user': 'deploy'
    },
    'sentinel10': {
        'service': 'sentinel10',
        'home': Path('/home/deploy/sentinel10/.und_mainchain'),
        'user': 'deploy'
    },
    'sentinel11': {
        'service': 'sentinel11',
        'home': Path('/home/deploy/sentinel11/.und_mainchain'),
        'user': 'deploy'
    },
    'sentinel12': {
        'service': 'sentinel12',
        'home': Path('/home/deploy/sentinel12/.und_mainchain'),
        'user': 'deploy'
    }
}


def get_defaults():
    d = {}
    for key, value in MACHINES.items():
        d[key] = {**value, **COMMON}
    return d
