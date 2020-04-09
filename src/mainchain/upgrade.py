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


def export_genesis(height, home):
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


def update_binaries():
    log.info('Updating Binaries')
    stdout = run_shell(f'curl -sfL https://git.io/JvHZO | sh')


def genesis_time(target: Path, new_time):
    contents = target.read_text()
    d = json.loads(contents)
    ts = d['genesis_time']
    log.info(f'Current genesis time is {ts}')
    d['genesis_time'] = new_time

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
        if height > h:
            log.info('Ready to upgrade')
            return
        else:
            log.info(f'Current height is {h}. Waiting')
            time.sleep(SLEEP_TIME)


def get_version():
    stdout = run_shell(f'/usr/local/bin/und version')
    log.info(stdout)


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
        machine = MACHINES['default']
    else:
        machine = MACHINES[machine]

    log.info(f"Stopping {machine['service']}")
    run_shell(f"systemctl stop {machine['service']}")

    unsafe_reset(machine['home'])
    fetch_genesis(machine['home'] / 'config/genesis.json')

    log.info(f"Starting {machine['service']}")
    run_shell(f"systemctl start {machine['service']}")


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
        machine = MACHINES['default']
    else:
        machine = MACHINES[machine]

    service = machine['service']
    home = machine['home']

    log.info(f'Stopping {service}')
    run_shell(f'systemctl stop {service}')

    intermediate = export_genesis(height, home)

    if genesistime is not None:
        log.info(f'Setting genesis time has been set to {genesistime}')
        intermediate = genesis_time(intermediate, genesistime)
        genesis = home / 'config/genesis.json'
        genesis.unlink()
        shutil.copy(str(intermediate), str(genesis.parent))
        log.info(f'The genesis has been copied')
    else:
        log.info(f'Genesis time has not been set')

    update_binaries()
    get_version()

    log.info(f'Starting {service}')
    run_shell(f'systemctl start {service}')


if __name__ == "__main__":
    main()
