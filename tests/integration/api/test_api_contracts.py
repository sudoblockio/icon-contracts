from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from icon_contracts.config import settings


def test_api_get_contracts(db: Session, client: TestClient):
    response = client.get(f"{settings.REST_PREFIX}/contracts").json()
    assert len(response) > 2
