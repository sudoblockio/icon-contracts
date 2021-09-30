import json
import os

import pytest

from icon_contracts.core.classifier import is_irc2

VALID_IRC2_CONTRACTS = [
    ("balanced_abi.json", True),
    ("act_abi.json", True),
    ("chihua_abi.json", True),
    ("idol_abi.json", False),
    ("irc2_abi_broken_name_schema.json", False),
    ("irc2_abi_broken_name_missing.json", False),
]


@pytest.mark.parametrize("fixture,validity", VALID_IRC2_CONTRACTS)
def test_irc2_accept(fixtures_dir, fixture, validity):
    with open(os.path.join(fixtures_dir, "abi", fixture)) as f:
        abi = json.load(f)

    classification = is_irc2(abi, "foo")
    assert classification == validity


CONTRACT_CLASSIFICATIONS = [
    ("cxf61cd5a45dc9f91c15aa65831a30a90d59a09619"),
]


def test_classify_contract():
    pass
