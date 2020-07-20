import logging
import os

import click

from undmainchain.common import stop, start, s3_sync
from undmainchain.const import get_defaults

log = logging.getLogger(__name__)


@click.group()
def main():
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))
    logging.getLogger("botocore").setLevel(logging.WARNING)
    logging.getLogger("s3transfer").setLevel(logging.WARNING)


@main.command()
@click.argument('access_key', required=True)
@click.argument('access_secret', required=True)
@click.option('-y', '--yes', required=False, is_flag=True)
@click.option('-m', '--machine', required=False, type=str, default=None)
def chain(access_key, access_secret, yes, machine):
    """
    Sync the Chain with Amazon S3

    """
    log.info('Sync Chain to Amazon S3')
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

    stop(machine_d)
    bucket = 'unification-mainchain'  # TODO: Try to generalise this
    s3_sync(access_key, access_secret, home, bucket)
    start(machine_d)


if __name__ == "__main__":
    main()
