import enum

class Status(enum.Enum):
    PENDING = "PENDING"
    PARTIAL = "PARTIAL"
    FILLED = "FILLED"
    CANCELED = "PARTIALLY CANCELED"