from server.data import Order, Status


class Exchange:
    def __init__(self, server):
        self.server = server
        self.orders_history = []
        self.order_book = [
            Order("SNAP", "BUY", "LMT", 30.50, 10),
            Order("SNAP", "BUY", "LMT", 30.00, 20),
            Order("SNAP", "BUY", "LMT", 29.00, 100),
            Order("SNAP", "SELL", "LMT", 31.00, 10),
            Order("SNAP", "SELL", "LMT", 31.50, 30),
            Order("SNAP", "SELL", "LMT", 29.00, 100),
            Order("FB", "BUY", "LMT", 25.00, 100),
            Order("FB", "SELL", "LMT", 26.00, 50),
        ]
        self.last_price = {
            "SNAP": 30.00,
            "FB": 26.00
        }

    def create_order(self, operation, ticker, order_type, price, quantity):
        order = Order(operation, ticker, order_type, price, quantity)
        self.orders_history.append(order)
        self.__execute_order(order)

    def __execute_order(self, order: Order):
        operation = "BUY" if order.operation == "SELL" else "SELL"
        filtered_order_book = filter(lambda item: item.ticker == order.ticker
                                     and item.operation == operation, self.order_book)

        # todo сортировка должна зависеть от стакана и поля price
        for order_item in sorted(filtered_order_book, key=lambda value: value.price):
            if order.quantity == order.filled_quantity:
                break

            if order_item.order_type == "LMT":
                if order_item.operation == "BUY" and order_item.price >= order.price:
                    break
                if order_item.operation == "SELL" and order_item.price <= order.price:
                    break

            can_take = min(order.quantity - order.filled_quantity,
                           order_item.quantity - order_item.filled_quantity)
            order_item.filled_quantity += can_take
            order.filled_quantity += can_take

            if order_item.quantity == order_item.filled_quantity:
                order_item.status = Status.FILLED
                self.order_book.remove(order_item)

        if order.quantity == order.filled_quantity:
            order.status = Status.FILLED
        else:
            if order.filled_quantity > 0:
                order.status = Status.PARTIAL

            if order.order_type == "LMT":
                self.order_book.append(order)
            elif order.order_type == "MKT":
                order.status = Status.CANCELED

    def get_quote(self, ticker):
        book = self.order_book.get(ticker)

        bid = max((order["price"] for order in book["BUY"]), default=None)
        ask = min((order["price"] for order in book["SELL"]), default=None)
        last = self.last_price.get(ticker, None)

        return {
            "bid": bid,
            "ask": ask,
            "last": last
        }

    def get_orders(self):
        return self.orders_history