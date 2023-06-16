from datetime import datetime
from typing import NamedTuple


class ReqParam(NamedTuple):
    token: str
    repo: str
    since: datetime
    until: datetime
