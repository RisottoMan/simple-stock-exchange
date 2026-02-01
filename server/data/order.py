from dataclasses import dataclass
from server.enum.status import Status


@dataclass
class Order:
    """Class for storing order data"""
    ticker: str
    operation: str
    order_type: str
    price: float
    quantity: int
    filled_quantity: int = 0
    status: Status = Status.PENDING

    def __post_init__(self):
        if self.price is not None:
            self.price = float(self.price)

    def __str__(self):
        price_display = f"${self.price:.2f} " if self.price is not None else ""

        return (
            f"{self.ticker} "
            f"{self.order_type} "
            f"{self.operation} "
            f"{price_display}"
            f"{self.filled_quantity}/{self.quantity} "
            f"{self.status.value}"
        )