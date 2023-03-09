from typing import Optional

import requests

from icon_contracts.config import settings
from icon_contracts.log import logger


def get_first_tx(address: str) -> Optional[int]:
    endpoint = settings.COMMUNITY_API_ENDPOINT + f"/api/v1/transactions?to={address}"
    r = requests.head(endpoint)
    if r.status_code == 200:
        total_records = int(dict(r.headers)["x-total-count"])
    else:
        logger.info(f"Could not head first tx {address}")
        return None

    skip = int(total_records / 100)
    endpoint = (
        settings.COMMUNITY_API_ENDPOINT + f"/api/v1/transactions?to={address}&skip={skip}&limit=100"
    )
    r = requests.get(endpoint)
    if r.status_code == 200:
        first_tx = r.json()[-1]["block_timestamp"]
        return first_tx

    logger.info(f"Could not head first tx {address}")
    return None
