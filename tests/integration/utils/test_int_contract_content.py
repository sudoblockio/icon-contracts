from icon_contracts.utils.contract_content import determine_s3_contract_key


def test_determine_s3_contract_key(init_secrets):
    x = determine_s3_contract_key("x")
