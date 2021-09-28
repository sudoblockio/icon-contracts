from icon_contracts.models.contracts import Contract


def test_db_basic_crud(db):
    contract = Contract(address="this")
    old_contract = contract.get(db)

    if not old_contract:
        db.add(contract)
        db.commit()

    new_contract = contract.get(db)
    assert new_contract


def test_db_basic_crud_new_item(db):
    from uuid import uuid4

    contract = Contract(address=str(uuid4()))

    db.add(contract)
    db.commit()

    new_contract = contract.get(db)
    assert new_contract
