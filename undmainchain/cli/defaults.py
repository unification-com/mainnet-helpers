import logging
import os

import click

from tabulate import tabulate

from undmainchain.const import get_defaults

log = logging.getLogger(__name__)


@click.group()
def main():
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    logging.getLogger("botocore").setLevel(logging.WARNING)
    logging.getLogger("s3transfer").setLevel(logging.WARNING)


@main.command()
@click.option('-m', '--machine', required=False, type=str, default=None)
def show(machine):
    """
    Show all the defaults
    """

    defaults = get_defaults()
    if machine is None:
        machine_d = defaults['default']
    else:
        machine_d = defaults[machine]

    s = sorted([(k, str(v)) for k, v in machine_d.items()], key=lambda x: x[0])
    print(tabulate(s))


if __name__ == "__main__":
    main()
