import json
import logging
import os
import subprocess
import tempfile
import time

import click

from pathlib import Path

from mainchain.sync import get_height

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
    cmd = f'curl -sfL https://git.io/JvHZO | sh'

    stdout = run_shell(cmd)


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


@click.group()
def main():
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))


@main.command()
@click.argument('height', required=True, type=int)
@click.argument('service', required=False)
@click.argument('home', required=False)
@click.argument('genesistime', required=False)
def genesis(height, service, home, genesistime):
    """
    Exports genesis, downloads new binaries, and restarts UND

    :param height:
    :param service:
    :param home:
    :param genesistime: Genesis time should be in the format: 2020-02-25T14:03:00Z
    :return:
    """
    log.info('Upgrading UND Mainchain')

    if home is None:
        home = Path(os.path.expanduser("~")) / '.und_mainchain'
    else:
        home = Path(home)

    if service is None:
        service = 'und'

    log.info(f'Stopping {service}')
    run_shell(f'systemctl stop {service}')

    intermediate = export_genesis(height, home)

    if genesistime is not None:

        log.info(f'Setting genesis time has been set to {genesistime}')
        intermediate = genesis_time(intermediate, genesistime)
    else:
        log.info(f'Genesis time has not been set')

    update_binaries()
    get_version()

    log.info(f'Starting {service}')
    run_shell(f'systemctl start {service}')


if __name__ == "__main__":
    main()
