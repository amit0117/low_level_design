from enum import StrEnum, auto

# StrEnum is used to create an enum class that stores strings as enum values
# Auto is used to create the lower case string value of the enum
# Benefit of using StrEnum is that we don't have to do .value to get the string value of the enum
# Like TaskStatus.TODO is "todo"

# Similar to this we can also have IntEnum.
# auto() with IntEnum will create an enum value from 1 to n automatically.

# Basically, using StrEnum and IntEnum we don't have to do .value to get the string value of the enum
# And auto() will automatically assign a unique value to the enum (for string it will assign the lower case string value, for int it will assign a unique value from 1 to n)


class TaskStatus(StrEnum):
    TODO = auto()
    IN_PROGRESS = auto()
    IN_REVIEW = auto()
    COMPLETED = auto()


class TaskPriority(StrEnum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    URGENT = auto()


# Tags are used to categorize tasks and can be used to filter tasks across different dimensions like pr
class TaskTag(StrEnum):
    # Priority Tags
    CRITICAL = auto()
    URGENT = auto()
    LOW_PRIORITY = auto()

    # Workflow/Status Tags
    NEEDS_REVIEW = auto()
    WAITING = auto()
    BLOCKED = auto()
    ON_HOLD = auto()

    # Context/Category Tags
    MEETING = auto()
    INTERNAL = auto()
    CLIENT_FACING = auto()
    BUG = auto()
    FEATURE = auto()

    # Energy/Effort Tags
    QUICK_WIN = auto()
    DEEP_WORK = auto()
