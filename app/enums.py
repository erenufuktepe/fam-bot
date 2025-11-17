import enum


class Cadence(str, enum.Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class Status(str, enum.Enum):
    PENDING = "pending"
    INPROGRESS = "in_progress"


class Month(str, enum.Enum):
    JANUARY = "january"
    FEBRUARY = "february"
    MARCH = "march"
    APRIL = "april"
    MAY = "may"
    JUNE = "june"
    JULY = "july"
    AUGUST = "august"
    SEPTEMBER = "september"
    OCTOBER = "october"
    NOVEMBER = "november"
    DECEMBER = "december"

    @classmethod
    def from_number(cls, num: int) -> "Month":
        """Convert month number (1–12) to enum."""
        members = list(cls)
        if 1 <= num <= len(members):
            return members[num - 1]
        raise ValueError(f"Invalid month number: {num}")

    @classmethod
    def from_string(cls, value: str | int) -> "Month":
        """Convert either a string ('january') or number (1) to enum."""
        if isinstance(value, int):
            return cls.from_number(value)

        if isinstance(value, str):
            value_lower = value.strip().lower()
            for month in cls:
                if month.value == value_lower or month.name.lower() == value_lower:
                    return month

        raise ValueError(f"Invalid month string or number: {value}")

    @property
    def number(self) -> int:
        """Get the month number (1–12) from the enum."""
        return list(self.__class__).index(self) + 1
