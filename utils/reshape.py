from datetime import datetime, timedelta
from typing import Any


def get_dict_val_by_key_order(
        src_dict: dict,
        reverse: bool = False,
) -> list[Any]:
    return [
        src_dict[key]
        for key in sorted(src_dict.keys(), reverse=reverse)
    ]


def get_year_week_list(
        since: datetime,
        until: datetime,
) -> list[str]:
    result = []
    while since <= until:
        calendar_date = since.isocalendar()
        year_and_week = f"{calendar_date.year}-{calendar_date.week}"
        result.append(year_and_week)
        since = since + timedelta(weeks=1)
    return result
