from datetime import time
from enum import StrEnum


class DaysOfWeek(StrEnum):
    MONDAY = "M"
    TUESDAY = "T"
    WEDNESDAY = "W"
    THURSDAY = "R"
    FRIDAY = "F"
    SATURDAY = "S"
    SUNDAY = "U"


DAYS_OF_WEEK_NAME = list(DaysOfWeek)


def format_time(time: time) -> str:
    s = ""
    s += str((time.hour % 12) or 12)
    if time.minute != 0:
        s += ":" + str(time.minute)
    if time.hour > 12:
        s += "pm"
    else:
        s += "am"
    return s
