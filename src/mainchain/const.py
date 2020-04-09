import os
from pathlib import Path

GENESIS = 'https://raw.githubusercontent.com/unification-com/testnet/master/latest/genesis.json'


MACHINES = {
    'default': {
        'service': 'und',
        'home': Path(os.path.expanduser("~")) / '.und_mainchain'
    },
    'shark': {
        'service': 'und',
        'home': Path('/home/deploy/.und_mainchain')
    }
}
