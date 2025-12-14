from enum import Enum

class TicketStatus(str, Enum):
    AVAILABLE = "available"
    SOLD = "sold"
    CANCELLED = "cancelled"