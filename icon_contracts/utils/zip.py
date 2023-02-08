"""Zip utility to prevent zip bombs"""
# https://stackoverflow.com/questions/13622706/how-to-protect-myself-from-a-gzip-or-bzip2-bomb
import contextlib
import resource
import zipfile

from icon_contracts.log import logger


@contextlib.contextmanager
def unzip_limit(limit, type=resource.RLIMIT_AS):
    soft_limit, hard_limit = resource.getrlimit(type)
    resource.setrlimit(type, (limit, hard_limit))  # set soft limit
    try:
        yield
    finally:
        resource.setrlimit(type, (soft_limit, hard_limit))  # restore


def unzip_safe(input_zip, output_dir, contract_hash=None):
    try:
        with unzip_limit(1 << 25):  # 32 Mb
            with zipfile.ZipFile(input_zip, "r") as zip_ref:
                # https://github.com/sudoblockio/icon-contracts/issues/6
                # size = sum(e.file_size for e in zip_ref.infolist())
                # if size
                zip_ref.extractall(output_dir)
    except MemoryError as e:
        logger.info(f"Contract hash upload is too large {contract_hash}.")
        raise e  # Caught in transactions.py
