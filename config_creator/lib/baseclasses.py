from enum import Enum

_all_ = ["ConnectionType"]


class ConnectionType(Enum):
    JOB = -1
    LOCAL = 0
    BIGQUERY = 1
    CSV = 2
    ORACLE = 3
