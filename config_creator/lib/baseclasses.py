from enum import Enum

_all_ = ["ConnectionType"]


class ConnectionType(Enum):
    BIGQUERY = 1
    CSV = 2
    ORACLE = 3
