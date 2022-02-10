from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class SocialMedia(SQLModel, table=True):
    """Social media details only filled in by contract verifications."""

    contract_address: str = Field(primary_key=True)

    team_name: Optional[str] = Field(None, index=False)
    short_description: Optional[str] = Field(None, index=False)
    long_description: Optional[str] = Field(None, index=False)
    p_rep_address: Optional[str] = Field(None, index=False)
    website: Optional[str] = Field(None, index=False)
    city: Optional[str] = Field(None, index=False)
    country: Optional[str] = Field(None, index=False)
    license: Optional[str] = Field(None, index=False)
    facebook: Optional[str] = Field(None, index=False)
    telegram: Optional[str] = Field(None, index=False)
    reddit: Optional[str] = Field(None, index=False)
    discord: Optional[str] = Field(None, index=False)
    steemit: Optional[str] = Field(None, index=False)
    twitter: Optional[str] = Field(None, index=False)
    youtube: Optional[str] = Field(None, index=False)
    github: Optional[str] = Field(None, index=False)
    keybase: Optional[str] = Field(None, index=False)
    wechat: Optional[str] = Field(None, index=False)

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "social_medias"
