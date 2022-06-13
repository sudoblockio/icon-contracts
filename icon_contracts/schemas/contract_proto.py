from icon_contracts.models.contracts import Contract
from icon_contracts.schemas.contract_processed_pb2 import ContractProcessed


def contract_to_proto(
    contract_db: Contract,
    contract_updated_block: int,
    contract_proto: ContractProcessed = None,
):
    """Convert a SQLModel contract to a protobuf."""
    if contract_proto is None:
        contract_proto = ContractProcessed()

    contract_proto.address = contract_db.address
    contract_proto.name = contract_db.name

    if contract_db.created_timestamp is not None:
        contract_proto.created_timestamp = int(contract_db.created_timestamp)

    if contract_db.status is not None:
        contract_proto.status = contract_db.status

    if contract_db.status is not None:
        contract_proto.status = contract_db.status

    if contract_db.token_standard is not None:
        contract_proto.token_standard = contract_db.token_standard

    contract_proto.contract_updated_block = contract_updated_block
    contract_proto.is_token = contract_db.is_token
    contract_proto.contract_type = contract_db.contract_type

    return contract_proto
