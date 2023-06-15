from datetime import datetime
from typing import NamedTuple


class ReqParam(NamedTuple):
    repo: str
    since: datetime
    until: datetime
