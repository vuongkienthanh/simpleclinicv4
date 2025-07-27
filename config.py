from paths import CFG_PATH
from typing import TypedDict, cast
import tomllib


class FollowChoice(TypedDict):
    name: str
    content: str


class Config(TypedDict):
    ## app
    font_size: int
    maximize_at_start: bool

    ## process
    checkup_price: int
    single_sale_units: list[str]
    default_follow_note: str
    follow_choices: list[FollowChoice]
    default_days_for_prescription: int
    min_warehouse_quantity_alert: int
    display_recent_visit_count: int  # -1 means no limit

    ## theme
    mainview: str


def get_config() -> Config:
    with open(CFG_PATH, "rb") as f:
        return cast(Config, tomllib.load(f))
