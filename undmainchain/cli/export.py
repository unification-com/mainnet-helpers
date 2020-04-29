import logging
import os
import subprocess
import tempfile
import time
from pathlib import Path

import click

from undmainchain.common import stop, upload_file, start
from undmainchain.const import get_defaults

log = logging.getLogger(__name__)


@click.group()
def main():
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))
    logging.getLogger("botocore").setLevel(logging.WARNING)
    logging.getLogger("s3transfer").setLevel(logging.WARNING)


@main.command()
@click.argument('height', required=True)
@click.argument('access_key', required=True)
@click.argument('access_secret', required=True)
@click.option('-y', '--yes', required=False, is_flag=True)
@click.option('-m', '--machine', required=False, type=str, default=None)
def genesis(height, access_key, access_secret, yes, machine):
    """
    Export the Genesis to Amazon S3

    """
    log.info('Exporting Genesis to Amazon S3')
    if yes is False:
        click.confirm('Do you want to continue?', abort=True)

    defaults = get_defaults()
    if machine is None:
        machine_d = defaults['default']
    else:
        machine_d = defaults[machine]

    home = machine_d['home']
    user = machine_d['user']

    stop(machine_d)

    td = tempfile.gettempdir()
    now = int(time.time())
    intermediate = Path(td) / f'genesis-{now}.json'
    compressed = Path(td) / f'genesis-{now}.json.gz'
    log.info(f'Writing to {intermediate}')

    export_cmd = f'/usr/local/bin/und export ' \
        f'--home {home}'
    cmd = f'runuser -l {user} -c "{export_cmd}"'

    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, shell=True,
        stderr=subprocess.PIPE, universal_newlines=True)

    log.debug(cmd)

    if result.returncode != 0:
        log.error(result.stdout)
        log.error(result.stderr)
        exit(1)

    intermediate.write_text(result.stdout)

    cmd = f'gzip {str(intermediate)}'

    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, shell=True,
        stderr=subprocess.PIPE, universal_newlines=True)

    if result.returncode != 0:
        log.error(result.stdout)
        log.error(result.stderr)
        exit(1)

    upload_file(access_key, access_secret, compressed, f'genesis-{now}.json.gz')

    start(machine_d)


@main.command()
@click.argument('access_key', required=True)
@click.argument('access_secret', required=True)
@click.option('-y', '--yes', required=False, is_flag=True)
@click.option('-m', '--machine', required=False, type=str, default=None)
def chain(access_key, access_secret, yes, machine):
    """
    Export the Chain to Amazon S3

    """
    log.info('Exporting Chain to Amazon S3')
    if yes is False:
        click.confirm(
            'Warning: this may consume a lot of data. '
            'Do you want to continue?', abort=True)

    defaults = get_defaults()
    if machine is None:
        machine_d = defaults['default']
    else:
        machine_d = defaults[machine]

    home = machine_d['home']

    td = tempfile.gettempdir()
    now = int(time.time())
    compressed = Path(td) / f'chain-{now}.gz'
    cmd = f'tar -cv {home} | gzip > {compressed}'
    log.info(cmd)

    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, shell=True,
        stderr=subprocess.PIPE, universal_newlines=True)

    if result.returncode != 0:
        log.error(result.stdout)
        log.error(result.stderr)
        exit(1)

    upload_file(access_key, access_secret, compressed, f'chain-{now}.json.gz')


if __name__ == "__main__":
    main()
