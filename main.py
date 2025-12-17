class Order:
    """Class for storing an order"""
    def __init__(self, side, ticker, order_type, price, filled_count, total_count, status):
        self.ticker = ticker
        self.order_type = order_type
        self.side = side
        self.price = price
        self.filled_count = filled_count
        self.total_count = total_count
        self.status = status

    def display_order(self):
        return (
            f"{self.ticker} "
            f"{self.order_type} "
            f"{self.side} "
            f"${self.price:.2f} "
            f"{self.filled_count}/{self.total_count} "
            f"{self.status} "
        ).upper()


class OrderManager:
    """Manager for processing user orders"""
    def __init__(self):
        self.orders = []

    def create_order(self, side, ticker, order_type, price, total_count):
        """Create a new order"""
        order = Order(side, ticker, order_type, price.lstrip("$"), 0, total_count, "pending")
        self.orders.append(order)
        print(f"You have placed a {order_type} {side} order for {total_count} {ticker} shares at {price} each.")

    def quite_order(self, *args):
        pass

    def view_orders(self):
        """Show all users orders"""
        for i, order in enumerate(self.orders, start=1):
            print(f"{i}. {order.display_order()}")


def main():
    """Client Application"""
    order = OrderManager()
    while True:
        command = input().strip().lower()
        args = command.split(" ")

        if args[0] == "buy" or args[0] == "sell":
            order.create_order(*args)
        elif command == "view orders":
            order.view_orders()
        elif args[0] == "quote":
            order.quite_order(*args)
        elif command == "quit":
            break
        else:
            print("Incorrect command")


if __name__ == "__main__":
    main()