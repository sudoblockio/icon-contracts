import filecmp
import io
import os
import shutil
import stat
import zipfile
from typing import Optional

import requests

from icon_contracts.config import settings
from icon_contracts.log import logger


def get_on_chain_contract_src(source_code_link) -> Optional[str]:
    """Request to s3 to get the zip."""
    r = requests.get(source_code_link)
    if r.status_code == 200:
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall("on_chain_source_code")
        return "on_chain_source_code"
    else:
        logger.info(f"Could not find {source_code_link}")
        return None


def get_file_list(root: str, file_list: list):
    """Get a list of files from a root dir."""
    for path, subdirs, files in os.walk(root):
        for name in files:
            file_list.append(os.path.join(path, name))


def compare_source(on_chain_dir, submitted_dir):
    """
    To compare the source, we assert that there are equal number of files and that each
    file matches each other using filecmp.
    https://stackoverflow.com/a/1072576/15781389
    """
    on_chain_files = []
    get_file_list(on_chain_dir, on_chain_files)

    submitted_dir_files = []
    get_file_list(submitted_dir, submitted_dir_files)

    try:
        assert len(submitted_dir_files) == len(on_chain_files)
    except AssertionError as e:
        logger.info("Extra file found in comparison.")
        raise e

    for i, f in enumerate(on_chain_files):
        try:
            assert filecmp.cmp(f, submitted_dir_files[i], shallow=False)
        except AssertionError as e:
            logger.info("Binaries don't match.")
            raise e


def replace_build_tool(verified_contract_path):
    """
    In the unlikely event someone modified the build tool, this would remove theirs and
    replace it with a known trusted copy.
    """
    gradlew_path = os.path.join(verified_contract_path, "gradlew")
    if os.path.isfile(gradlew_path):
        os.remove(gradlew_path)

    gradle_wrapper_path = os.path.join(verified_contract_path, "gradle")
    if os.path.isdir(gradle_wrapper_path):
        shutil.rmtree(gradle_wrapper_path)

    src = os.path.join(settings.GRADLE_PATH, "gradle")
    dest = os.path.join(verified_contract_path, "gradle")
    shutil.copytree(src, dest)

    src = os.path.join(settings.GRADLE_PATH, "gradlew")
    dest = os.path.join(verified_contract_path, "gradlew")
    shutil.copyfile(src, dest)

    # chmod +x gradlew
    st = os.stat(dest)
    os.chmod(dest, st.st_mode | stat.S_IEXEC)
