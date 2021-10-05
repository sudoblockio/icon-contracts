from icon_contracts.api.db import get_session
from fastapi import Depends


def is_database_online(session: bool = Depends(get_session)):
    return session
