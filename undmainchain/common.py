import logging
from pathlib import Path

import boto3

from undmainchain.const import DEFAULT_BUCKET
from undmainchain.sync import run_shell

log = logging.getLogger(__name__)


def stop(machine_d):
    log.info(f"Stopping {machine_d['service']}")
    run_shell(f"systemctl stop {machine_d['service']}")


def start(machine_d):
    log.info(f"Starting {machine_d['service']}")
    run_shell(f"systemctl start {machine_d['service']}")


def upload_file(
        access_key, access_secret, local: Path, remote: str, bucket=None):
    s3_client = boto3.client('s3', aws_access_key_id=access_key,
                             aws_secret_access_key=access_secret)

    if bucket is None:
        bucket = DEFAULT_BUCKET
    response = s3_client.upload_file(
        str(local), bucket, remote)

    log.info(f'Uploaded {remote}')
