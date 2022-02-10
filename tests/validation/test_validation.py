import pytest
import requests

ENVIRONMENTS = [
    # (
    #     "dev",
    #     "mainnet",
    #     "explorer.icon.geometry-dev.net"
    # ),
    ("prod-us-west-2", "mainnet", "tracker.icon.community"),
    # (
    #     "prod-eu-west-1",
    #     "mainnet",
    "euw1.tracker.icon.community"
    # ),
]


@pytest.mark.parametrize("environment,network,base_url", ENVIRONMENTS)
def test_contract_counts(client, environment, network, base_url):
    base_url = "https://" + base_url + "/api/v1/"
    contracts_url = base_url + "contracts"
    addresses_url = base_url + "addresses/contracts"

    contracts_response = requests.get(contracts_url, headers={"content-type": "text"})
    assert contracts_response

    addresses_response = requests.get(addresses_url).json()
    assert addresses_response
