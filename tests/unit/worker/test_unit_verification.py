import json
import os
import shutil
import subprocess

import pytest

from icon_contracts.models.verification_contract import VerificationInput
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


# Copying in gradle now so this is not needed
# def test_error_subprocess_gradlew(fixtures_dir):
#     """Make sure our error handling is ok with subprocess calling gradlew."""
#     verified_contract_path = os.path.join(fixtures_dir, "java_contracts", "src")
#     os.chdir(verified_contract_path)
#     subprocess.call([os.path.join(verified_contract_path, "gradlew"), "optimizedJar"])
#     shutil.rmtree(os.path.join(verified_contract_path, "contracts", "build"))


def test_regex_validator_verification(fixtures_dir):
    """Make sure the validators don't allow more than one word."""
    v = VerificationInput(
        gradle_task="foo",
        gradle_target="bar",
    )
    assert v.gradle_target == "bar"


BAD_TARGETS = ["bar(bar", "bar`curl ht`bar"]


@pytest.mark.parametrize("target", BAD_TARGETS)
def test_regex_validator_verification_fails(target, fixtures_dir):
    """Make sure the validators don't allow more than one word."""
    with pytest.raises(ValueError):
        VerificationInput(
            gradle_task="foo",
            gradle_target=target,
        )


BAD_GH_REFS = ["bar(bar", "bar`curl ht`bar"]


@pytest.mark.parametrize("target", BAD_GH_REFS)
def test_regex_validator_verification_fails_gh(target, fixtures_dir):
    """Make sure the validators don't allow more than one word."""
    with pytest.raises(ValueError):
        VerificationInput(
            github_org=target,
        )


GOOD_GH_REFS = ["barbar", "bar-bar", "Bar_bar1"]


@pytest.mark.parametrize("target", GOOD_GH_REFS)
def test_regex_validator_verification_works(target, fixtures_dir):
    """Make sure the validators don't allow more than one word."""
    v = VerificationInput(github_org=target)

    assert v


GOOD_GH_RELEASES = ["v0.1.1", "v0.1.1-alpha.1"]


@pytest.mark.parametrize("target", GOOD_GH_RELEASES)
def test_regex_validator_verification_release_works(target, fixtures_dir):
    """Make sure the validators don't allow more than one word."""
    v = VerificationInput(github_release=target)

    assert v


@pytest.mark.parametrize("tx_fixture", ["zip-source-v1.json", "github-source-v1.json"])
def test_tx_fixtures(chdir_fixtures, tx_fixture):
    os.chdir("java_contracts")
    with open(tx_fixture) as f:
        params = json.load(f)

    v = VerificationInput(**params)
    assert v
