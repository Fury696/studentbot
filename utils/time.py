from typing import Union
from time import struct_time
from enum import Enum
import arrow
import datetime

TIMESTAMP = Union[
    arrow.Arrow,
    datetime.datetime,
    datetime.date,
    struct_time,
    int,  # POSIX timestamp
    float,  # POSIX timestamp
    str,  # ISO 8601-formatted string
    tuple[int, int, int],  # ISO calendar tuple
]

class TimestampFormats(Enum):
    DATE_TIME = "f"  # January 1, 1970 1:00 AM
    DAY_TIME = "F"  # Thursday, January 1, 1970 1:00 AM
    DATE_SHORT = "d"  # 01/01/1970
    DATE = "D"  # January 1, 1970
    TIME = "t"  # 1:00 AM
    TIME_SECONDS = "T"  # 1:00:00 AM
    RELATIVE = "R"  # 52 years ago

def timestamp(timestamp: TIMESTAMP) -> int:
    return int(arrow.get(timestamp).timestamp())

def discord_timestamp(
    timestamp: TIMESTAMP,
    format: TimestampFormats = TimestampFormats.DATE_TIME
) -> str:
    timestamp = int(arrow.get(timestamp).timestamp())
    return f"<t:{timestamp}:{format.value}>"