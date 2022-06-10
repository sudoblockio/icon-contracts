from typing import List


def contract_classifier(abi: List[dict], contract_spec: List[dict]) -> bool:
    try:
        abi_methods = [m["name"] for m in abi]
    except TypeError:
        # We are missing ABIs for some approved contracts
        return False
    for i in contract_spec:
        if i["name"] not in abi_methods:
            # Method does not exist in the token standard
            return False

        schema = [m for m in abi if m["name"] == i["name"]][0]
        if i != schema:
            # Make sure the method schema matches the token standard
            return False

    return True
