import pytest

from icon_contracts.workers.transactions import transactions_worker


@pytest.fixture()
def contract_creation_docker(docker_up_block, docker_project_down):
    # https://tracker.icon.foundation/transaction/0x9340d53058aa3323ffd1cf5d7213f06350460e530f24af3c095b681aa8896ac4
    project = docker_up_block("33518615")
    yield
    # docker_project_down(project)


# def test_contract_creation_python(db):
#     transactions_worker(session=db)
