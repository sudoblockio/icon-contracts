import pytest
from icon_contracts.workers.transactions import transactions_worker




@pytest.fixture()
def contract_creation_docker(docker_up_block, docker_project_down):
    project = docker_up_block("62000")
    yield
    docker_project_down(project)


def test_contract_creation_python(contract_creation_docker):
    # transactions_worker()
    print()
