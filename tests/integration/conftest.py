import os

from typing import Generator
import pytest
from compose.cli.command import project_from_options
from compose.service import ImageType

from icon_contracts.db import get_session
from icon_contracts.models.contracts import Contract

pytest_plugins = ["docker_compose"]


@pytest.fixture(scope="session")
def db() -> Generator:
    yield get_session()


@pytest.fixture()
def init_db(db):
    with db:
        db.query(Prep)


@pytest.fixture()
def get_path_to_file():
    def f(file_name):

        cur_dir = os.getcwd()

        while True:
            file_list = os.listdir(cur_dir)
            parent_dir = os.path.dirname(cur_dir)

            if file_name in file_list:
                return cur_dir
            else:
                if cur_dir == parent_dir:
                    break
                else:
                    cur_dir = parent_dir

    return f

@pytest.fixture()
def get_compose_project(get_path_to_file):

    def f(compose_files=None):
        if compose_files is None:
            compose_files = ['docker-compose.yml', 'docker-compose.db.yml']

        project_dir = get_path_to_file(compose_files[0])

        project = project_from_options(
            project_dir=str(project_dir),
            options={"--file": compose_files},
        )
        return project
    return f


@pytest.fixture()
def docker_up_block(get_compose_project):

    def f(block, compose_files=None):
        get_compose_project(compose_files)
        os.environ['START_BLOCK'] = block

        project = get_compose_project()
        project.up()

        return project
    return f

@pytest.fixture()
def docker_project_down(get_compose_project):
    def f(project):
        project.down(ImageType.none, "--docker-compose-remove-volumes")
    return f
