from dataclasses import dataclass


@dataclass
class Order:
    """Class for storing order data"""
    operation: str
    ticker: str
    order_type: str
    price: float
    quantity: int
    filled_quantity: int = 0
    status: str = "PENDING"

    def __post_init__(self):
        if self.price is not None:
            self.price = float(self.price)

        self.quantity = int(self.quantity)

    def __str__(self):
        price_display = f"${self.price:.2f} " if self.price is not None else ""

        return (
            f"{self.ticker} "
            f"{self.order_type} "
            f"{self.operation} "
            f"{price_display}"
            f"{self.filled_quantity}/{self.quantity} "
            f"{self.status}"
        )


class Server:
    """Server for processing client requests"""
    def __init__(self):
        self.orders = []

    def handle(self, command: str) -> str:
        """Request handler"""
        parts = command.strip().upper().split()
        if not parts:
            return "EMPTY COMMAND"

        cmd = parts[0]

        if cmd == "BUY" or cmd == "SELL":
            return self.create_order(*parts)

        if cmd == "VIEW":
            return self.view_orders()

        if cmd == "QUOTE":
            return self.get_quote(parts[1])

        return "UNKNOWN COMMAND"

    def create_order(self, *parts) -> str:
        """Creating a new order"""
        if len(parts) == 5:
            operation, ticker, order_type, price, quantity = parts
            price = price.lstrip("$")
        elif len(parts) == 4:
            operation, ticker, order_type, quantity = parts
            price = None
        else:
            return "INVALID COMMAND"

        if operation not in {"BUY", "SELL"}:
            return "INVALID OPERATION"

        if order_type not in {"LMT", "MKT"}:
            return "INVALID ORDER TYPE"

        order = Order(operation, ticker, order_type, price, quantity)
        self.orders.append(order)

        if order_type == "LMT":
            return f"You have placed a limit {operation.lower()} order for {quantity} {ticker} shares at ${float(price):.2f} each."
        else:
            return f"You have placed a market order for {quantity} {ticker} shares."

    def get_quote(self, ticker) -> str:
        """Get information about quotes"""
        return f"{ticker} BID: $30.00 ASK: $31.00 LAST: $30.00"

    def view_orders(self) -> str:
        """Show all orders"""
        result_lines = []
        for i, order in enumerate(self.orders, start=1):
            result_lines.append(f"{i}. {order}")
        return "\n".join(result_lines)


class Client:
    """Client for sending requests to the server"""
    def __init__(self, server: Server):
        self.server = server

    def send(self, command):
        """Send a request"""
        response = self.server.handle(command)
        return response


def main():
    server = Server()
    client = Client(server)

    while True:
        command = input("Action: ")
        if command == "QUIT":
            break

        result = client.send(command)
        print(result, "\n")


if __name__ == "__main__":
    main()