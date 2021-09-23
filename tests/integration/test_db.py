from icon_contracts.models.contracts import Contract


def test_db(db, sample_contract):
    db.add(sample_contract)
    db.commit()


def test_this(db):
    c = Contract(address="this")
    z = c.get(db)
    print()
