import os
import shutil
import subprocess

import pytest

from icon_contracts.workers.verification import compare_source


def test_compare_source(fixtures_dir):
    """Run assertions inside function - fail otherwise."""
    os.chdir(os.path.join(fixtures_dir, "java_contracts", "comparison", "success"))
    compare_source("source_code", "verified_jar")


@pytest.mark.parametrize("fixture", ["fail-extra-file", "fail-different-bin"])
def test_compare_source_fail(fixtures_dir, fixture):
    """Run assertions inside function - fail otherwise."""
    os.chdir(os.path.join(fixtures_dir, "java_contracts", "comparison", fixture))
    with pytest.raises(AssertionError):
        compare_source("source_code", "verified_jar")


def test_error_subprocess_gradlew(fixtures_dir):
    """Make sure our error handling is ok with subprocess calling gradlew."""
    verified_contract_path = os.path.join(fixtures_dir, "java_contracts", "src")
    os.chdir(verified_contract_path)
    subprocess.call([os.path.join(verified_contract_path, "gradlew"), "optimizedJar"])
    shutil.rmtree(os.path.join(verified_contract_path, "contracts", "build"))
