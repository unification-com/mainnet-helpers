import json
import logging
import os
import shutil
import subprocess
import tempfile
import time

import click

from pathlib import Path

from mainchain.sync import get_height, fetch_genesis
from mainchain.const import MACHINES

log = logging.getLogger(__name__)

SLEEP_TIME = 5


def run_shell(cmd):
    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, shell=True,
        stderr=subprocess.PIPE, universal_newlines=True)

    log.debug(cmd)

    if result.returncode != 0:
        log.error(result.stdout)
        log.error(result.stderr)
        exit(1)

    return result.stdout


def export_genesis(machine_d, height):
    home = machine_d['home']
    log.info('Exporting genesis')
    cmd = f'/usr/local/bin/und export ' \
        f'--for-zero-height --height {height} --home {home}'

    stdout = run_shell(cmd)

    td = tempfile.gettempdir()
    now = int(time.time())
    intermediate = Path(td) / f'genesis-{now}.json'

    log.info(f'Writing to {intermediate}')
    intermediate.write_text(stdout)
    return intermediate


def replace_genesis(machine_d, source):
    home = machine_d['home']
    target = home / 'config/genesis.json'
    target.unlink()
    shutil.copy(str(source), str(target.parent))
    log.info(f'The genesis has been copied')


def update_binaries():
    log.info('Updating Binaries')
    stdout = run_shell(f'curl -sfL https://git.io/JvHZO | sh')


def genesis_time(target: Path, new_time):
    contents = target.read_text()
    d = json.loads(contents)
    ts = d['genesis_time']
    log.info(f'Current genesis time is {ts}')
    d['genesis_time'] = new_time
    d['chain_id'] = "UND-Mainchain-TestNet-v4" #TODO: Extract

    td = tempfile.gettempdir()
    now = int(time.time())
    target = Path(td) / f'genesis-{now}.json'

    target.write_text(json.dumps(d, indent=2, separators=(',', ': ')))
    log.info(f'Writing to {target}')
    return target


def wait_for_height(height):
    """
    TODO: The service might not be running
    """
    while True:
        h = get_height()
        if h > height:
            log.info('Ready to upgrade')
            return
        else:
            log.info(f'Current height is {h}. Waiting')
            time.sleep(SLEEP_TIME)


def get_version():
    stdout = run_shell(f'/usr/local/bin/und version')
    log.info(stdout)


def stop(machine_d):
    log.info(f"Stopping {machine_d['service']}")
    run_shell(f"systemctl stop {machine_d['service']}")


def start(machine_d):
    log.info(f"Starting {machine_d['service']}")
    run_shell(f"systemctl start {machine_d['service']}")


def unsafe_reset(home):
    log.info('Unsafe Reset All')
    stdout = run_shell(f'/usr/local/bin/und unsafe-reset-all --home {home}')
    log.info(stdout)


@click.group()
def main():
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))


@main.command()
@click.argument('machine', required=False)
def revert(machine):
    log.info('Reverting UND Mainchain')
    click.confirm('Do you want to continue?', abort=True)

    if machine is None:
        machine_d = MACHINES['default']
    else:
        machine_d = MACHINES[machine]

    stop(machine_d)

    unsafe_reset(machine['home'])
    fetch_genesis(machine['home'] / 'config/genesis.json')

    start(machine_d)


@main.command()
@click.argument('height', required=True, type=int)
@click.argument('genesistime', required=False)
@click.argument('machine', required=False)
def genesis(height, genesistime, machine):
    """
    Exports genesis, downloads new binaries, and restarts UND

    :param height:
    :param genesistime: Genesis time should be in the format: 2020-02-25T14:03:00Z
    :return:
    """
    log.info('Upgrading UND Mainchain')

    if machine is None:
        machine_d = MACHINES['default']
    else:
        machine_d = MACHINES[machine]

    service = machine_d['service']
    home = machine_d['home']

    wait_for_height(height)

    stop(machine_d)

    intermediate = export_genesis(machine_d, height)

    if genesistime is not None:
        log.info(f'Setting genesis time has been set to {genesistime}')
        intermediate = genesis_time(intermediate, genesistime)
        replace_genesis(machine_d, intermediate)
    else:
        log.info(f'Genesis time has not been set')

    update_binaries()
    get_version()

    start(machine_d)


if __name__ == "__main__":
    main()
