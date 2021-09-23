import tempfile
import os
import zipfile
from icon_contracts.utils.shell import run_command
from icon_contracts.schemas.transaction_raw_pb2 import TransactionRaw


def unzip_content_to_dir(content: str, txn_hash: str) -> str:
    if content.startswith("0x"):
        content = content[2:]

    dirpath = tempfile.mkdtemp()
    contract_path = os.path.join(dirpath, txn_hash)
    with open(contract_path + '.txt', 'w') as f:
        f.write(content)

    command = f'xxd -r -p {contract_path}.txt > {contract_path}.zip'
    run_command(command)

    with zipfile.ZipFile(contract_path + '.zip', "r") as zip_ref:
        zip_ref.extractall(dirpath)

    files = os.listdir(dirpath)
    for f in files:
        if os.path.isdir(os.path.join(dirpath, f)):
            break

    return os.path.join(dirpath, f)


def import_score(score_dir):
    pass