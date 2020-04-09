import requests

from pathlib import Path

from mainchain.const import GENESIS


def get_height():
    r = requests.get('http://localhost:26657/status')
    d = r.json()

    height = int(d['result']['sync_info']['latest_block_height'])
    return height


def fetch_genesis(target: Path):
    r = requests.get(GENESIS)
    target.write_text(r.text)
