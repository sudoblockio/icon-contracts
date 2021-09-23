from fastapi.testclient import TestClient
from icon_contracts.config import settings

from sqlalchemy.orm import Session


def test_api_get_contracts(db: Session, client: TestClient):
    response = client.get(f"{settings.REST_PREFIX}/contracts").json()
    print()
