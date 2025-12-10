import logging
from datetime import datetime
from zoneinfo import ZoneInfo

logger = logging.getLogger(__name__)

TZ = ZoneInfo("America/Chicago")


def get_current_month() -> int:
    return datetime.now(TZ).month


def get_current_year() -> int:
    return datetime.now(TZ).year


def get_current_datetime() -> datetime:
    return datetime.now(TZ)


def validate_mmdd_format(date_str: str) -> bool:
    try:
        format_code = "%m/%d"
        datetime.strptime(f"2000/{date_str}", f"%Y/{format_code}")
        return True
    except ValueError as exc:
        logger.exception(f"Value error: {exc}")
        return False
    except TypeError as exc:
        logger.exception(f"Type error: {exc}")
        return False


def validate_datetime(date_str: str) -> bool:
    try:
        _datetime = datetime.strptime(date_str, "%Y/%m/%d %H:%M")
        is_valid = (
            True if _datetime > get_current_datetime().replace(tzinfo=None) else False
        )
        return is_valid
    except ValueError:
        return False


def to_datetime(date_str: str) -> datetime:
    try:
        return datetime.strptime(date_str, "%Y/%m/%d %H:%M")
    except ValueError as exc:
        raise ValueError(f"Invalid datetime: {exc}")


def parse_mmdd_format(date_str: str) -> tuple[int, int]:
    try:
        date = date_str.split("/")
        if len(date) != 2:
            raise ValueError("Date must be in MM/DD format")
        month = int(date[0])
        day = int(date[1])
        return month, day
    except ValueError as exc:
        raise ValueError(f"Invalid date format: {exc}")
