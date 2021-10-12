import pytest
from dotenv import load_dotenv


@pytest.fixture()
def load_environment_variables(chdir_base):
    load_dotenv()
    yield
