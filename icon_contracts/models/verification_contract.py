import re

from pydantic import BaseModel, validator


class VerificationInput(BaseModel):
    """Social media details only filled in by contract verifications."""

    contract_address: str = ""

    team_name: str = ""
    short_description: str = ""
    long_description: str = ""
    p_rep_address: str = ""
    website: str = ""
    city: str = ""
    country: str = ""
    license: str = ""
    facebook: str = ""
    telegram: str = ""
    reddit: str = ""
    discord: str = ""
    steemit: str = ""
    twitter: str = ""
    youtube: str = ""
    github: str = ""
    keybase: str = ""
    wechat: str = ""

    gradle_target: str = ""
    gradle_task: str = ""

    source_code_location: str = ""
    zipped_source_code: str = ""

    @validator("gradle_target", "gradle_task")
    def check_only_one_word(cls, v):
        if v == "":
            return v
        single_word_regex = r"^[a-zA-Z0-9]+$"
        if not re.match(single_word_regex, v):
            raise ValueError(f"Value {v} does not match regex {single_word_regex}")
        else:
            return v

    @validator("gradle_task")
    def gradle_task_populate_optimizedJar_if_empty(cls, v):
        if v == "":
            return "optimizedJar"
        return v

    @validator("zipped_source_code")
    def starts_with_0x(cls, v):
        if not v.startswith("0x"):
            raise ValueError(f"Value {v} does not start with 0x")
        else:
            return v
