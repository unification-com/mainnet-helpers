import logging
import os
import subprocess
import tempfile
import time
from pathlib import Path

import click

from undmainchain.const import get_defaults

log = logging.getLogger(__name__)


def line_in_file(target, prefix, replacement):
    contents = target.read_text()
    newlines = []
    for line in contents.splitlines():
        if line.startswith(prefix + " "):
            newline = f'{prefix} = {replacement}'
            newlines.append(newline)
        else:
            newlines.append(line)

    target.write_text('\n'.join(newlines))


def read_line_in_file(target, prefix):
    contents = target.read_text()
    for line in contents.splitlines():
        if line.startswith(prefix + " "):
            splitted = line.split('"')
            return splitted[1]


@click.group()
def main():
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))


@main.command()
@click.argument('line', required=True)
@click.argument('value', required=True)
@click.option('-y', '--yes', required=False, is_flag=True)
@click.option('-m', '--machine', required=False, type=str, default=None)
def set_app(line, value, yes, machine):
    """
    Change a line in the app.toml

    """
    log.info('Re-writing config file')
    if yes is False:
        click.confirm('Do you want to continue?', abort=True)

    defaults = get_defaults()
    if machine is None:
        machine_d = defaults['default']
    else:
        machine_d = defaults[machine]

    home = machine_d['home']
    user = machine_d['user']


@main.command()
@click.argument('line', required=True)
@click.option('-y', '--yes', required=False, is_flag=True)
@click.option('-m', '--machine', required=False, type=str, default=None)
def read_app(value, yes, machine):
    """
    Read a value in the app.toml

    """
    defaults = get_defaults()
    if machine is None:
        machine_d = defaults['default']
    else:
        machine_d = defaults[machine]

    home = machine_d['home']

    app_config = home / 'config/app.toml'
    value = read_line_in_file(app_config, value)

    print(value)


if __name__ == "__main__":
    main()
