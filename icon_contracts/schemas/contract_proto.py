from icon_contracts.models.contracts import Contract
from icon_contracts.schemas.contract_processed_pb2 import ContractProcessed


def contract_to_proto(
    contract_db: Contract,
    contract_updated_block: int,
    is_creation: bool,
    contract_proto: ContractProcessed = None,
):
    """Convert a SQLModel contract to a protobuf."""
    if contract_proto is None:
        contract_proto = ContractProcessed()

    contract_proto.address = contract_db.address

    if contract_db.name is not None:
        contract_proto.name = contract_db.name

    if contract_db.created_timestamp is not None:
        contract_proto.created_timestamp = int(contract_db.created_timestamp)

    if contract_db.status is not None:
        contract_proto.status = contract_db.status

    if contract_db.symbol is not None:
        contract_proto.symbol = contract_db.symbol

    if contract_db.token_standard is not None:
        contract_proto.token_standard = contract_db.token_standard

    if contract_db.contract_type is not None:
        contract_proto.contract_type = contract_db.contract_type

    contract_proto.is_token = contract_db.is_token

    # Tx related
    if contract_updated_block is not None:
        contract_proto.contract_updated_block = contract_updated_block

    contract_proto.contract_updated_block = contract_updated_block
    # contract_proto.contract_updated_hash = contract_updated_hash
    contract_proto.is_creation = is_creation

    return contract_proto
