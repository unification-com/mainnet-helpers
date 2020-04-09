import requests


def get_height():
    r = requests.get('http://localhost:26657/status')
    d = r.json()

    height = int(d['result']['sync_info']['latest_block_height'])
    return height
