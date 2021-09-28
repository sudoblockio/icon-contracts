import json
import os
import tempfile
import zipfile
from pathlib import Path
from typing import Union

from icon_contracts.schemas.transaction_raw_pb2 import TransactionRaw
from icon_contracts.utils.shell import run_command


def unzip_content_to_dir(content: str, txn_hash: str) -> str:
    if content.startswith("0x"):
        content = content[2:]

    dirpath = tempfile.mkdtemp()
    contract_path = os.path.join(dirpath, txn_hash)
    with open(contract_path + ".txt", "w") as f:
        f.write(content)

    command = f"xxd -r -p {contract_path}.txt > {contract_path}.zip"
    run_command(command)

    with zipfile.ZipFile(contract_path + ".zip", "r") as zip_ref:
        zip_ref.extractall(dirpath)

    files = os.listdir(dirpath)
    for f in files:
        if os.path.isdir(os.path.join(dirpath, f)):
            break

    return os.path.join(dirpath, f)


def import_score(score_dir):
    pass


def find_and_load_package_json(contract_path) -> Union[dict, NotADirectoryError]:
    # Find the path to the first package.json
    for path in Path(contract_path).rglob("package.json"):
        # Extract the package_json
        with open(path) as file:
            return json.load(file)
    return NotADirectoryError(f"Could not find package.json in {contract_path}")


if __name__ == "__main__":
    x = find_and_load_package_json("/tmp/tmpci_lmje5/")
    print()
