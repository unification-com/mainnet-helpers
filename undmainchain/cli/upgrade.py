import json
import logging
import os
import shutil
import tempfile
import time
from pathlib import Path

import click

from undmainchain.common import start, stop
from undmainchain.const import get_defaults
from undmainchain.sync import get_height, fetch_genesis, run_shell

log = logging.getLogger(__name__)

SLEEP_TIME = 5


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
    run_shell(f'sh -c "$(curl -sfSL https://git.io/JvHZO)"')


def update_binaries_specific(version):
    for item in ['und', 'undcli']:
        td = tempfile.gettempdir()
        target = Path(td) / f'{item}.tar.gz'
        if target.exists():
            target.unlink()

        log.debug(f'Downloading to {target}')
        run_shell(
            f'wget https://github.com/unification-com/mainchain/releases/'
            f'download/{version}/{item}_v{version}_linux_x86_64.tar.gz -O '
            f'{target}')
        run_shell(f'tar -xC /usr/local/bin -f {target}')
        run_shell(f'chmod + /usr/local/bin/{item}')


def genesis_time(target: Path, new_time, new_chain_id):
    contents = target.read_text()
    d = json.loads(contents)
    ts = d['genesis_time']
    log.info(f'Current genesis time is {ts}')
    d['genesis_time'] = new_time
    d['chain_id'] = new_chain_id

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


def unsafe_reset(machine_d):
    home = machine_d['home']
    user = machine_d['user']

    log.info('Unsafe Reset All')
    stdout = run_shell(
        f'runuser -l {user} -c "'
        f'/usr/local/bin/und unsafe-reset-all --home {home}"')
    log.info(stdout)


@click.group()
def main():
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))
    logging.getLogger("botocore").setLevel(logging.WARNING)
    logging.getLogger("s3transfer").setLevel(logging.WARNING)


@main.command()
@click.argument('version', required=True, type=str)
@click.option('-y', '--yes', required=False, is_flag=True)
@click.option('-m', '--machine', required=False, type=str, default=None)
def binaries(version, yes, machine):
    """
    Fetches the specified version of the UND binaries

    """
    click.echo(f'Installing UND binaries version {version} from '
               f'https://github.com/unification-com/mainchain/releases')
    if yes is False:
        click.confirm('Do you want to continue?', abort=True)

    defaults = get_defaults()
    if machine is None:
        machine_d = defaults['default']
    else:
        machine_d = defaults[machine]

    stop(machine_d)

    update_binaries_specific(version)

    get_version()

    start(machine_d)


@main.command()
@click.option('-y', '--yes', required=False, is_flag=True)
@click.option('-m', '--machine', required=False, type=str, default=None)
def reset(yes, machine):
    """
    Reset all data, fetches the latest binary, and uses the latest published
    genesis. Use this if you want to restart from a fresh slate.

    :param machine: Override default locations for a particular machine
    :return:
    """
    click.echo('Reverting UND Mainchain')
    if yes is False:
        click.confirm('Do you want to continue?', abort=True)

    defaults = get_defaults()
    if machine is None:
        machine_d = defaults['default']
    else:
        machine_d = defaults[machine]

    stop(machine_d)

    update_binaries()
    get_version()

    unsafe_reset(machine_d)
    fetch_genesis(machine_d)

    start(machine_d)


@main.command()
@click.argument('height', required=True, type=int)
@click.argument('genesistime', required=False)
@click.argument('chain_id', required=False)
@click.option('-m', '--machine', required=False, type=str, default=None)
def genesis(height, genesistime, chain_id, machine):
    """
    Exports genesis, downloads new binaries, and restarts UND

    :param height:
    :param genesistime: Genesis time should be in the format: 2020-02-25T14:03:00Z
    :param chain_id:
    :param machine: Override default locations for a particular machine
    """
    click.echo('Upgrading UND Mainchain')

    defaults = get_defaults()
    if machine is None:
        machine_d = defaults['default']
    else:
        machine_d = defaults[machine]

    wait_for_height(height)

    stop(machine_d)

    intermediate = export_genesis(machine_d, height)

    if genesistime is not None:
        log.info(f'Setting genesis time has been set to {genesistime}')
        intermediate = genesis_time(intermediate, genesistime, chain_id)
        replace_genesis(machine_d, intermediate)
    else:
        log.info(f'Genesis time has not been set')

    unsafe_reset(machine_d)

    update_binaries()
    get_version()

    start(machine_d)


if __name__ == "__main__":
    main()
