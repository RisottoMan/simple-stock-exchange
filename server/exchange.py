from server.data import Order, Status


class Exchange:
    def __init__(self, server):
        self.server = server
        self.orders_history = []
        self.order_book = []

    def create_order(self, ticker, operation, order_type, price, quantity):
        order = Order(ticker, operation, order_type, price, quantity)
        self.orders_history.append(order)
        self.__execute_order(order)

    def __execute_order(self, order: Order):
        operation = "BUY" if order.operation == "SELL" else "SELL"
        is_reverse = (operation == "BUY")
        filtered_order_book = filter(lambda item: item.ticker == order.ticker
                                     and item.operation == operation, self.order_book)

        for order_item in sorted(filtered_order_book, key=lambda value: value.price, reverse=is_reverse):
            if order.quantity == order.filled_quantity:
                break

            if order.order_type == "LMT":
                if order.operation == "BUY" and order_item.price > order.price:
                    break
                if order.operation == "SELL" and order_item.price < order.price:
                    break

            can_take = min(order.quantity - order.filled_quantity,
                           order_item.quantity - order_item.filled_quantity)
            order_item.filled_quantity += can_take
            order.filled_quantity += can_take

            if order_item.quantity == order_item.filled_quantity:
                order_item.status = Status.FILLED
                self.order_book.remove(order_item)
            elif order_item.quantity > 0:
                order_item.status = Status.PARTIAL

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
        order_book = [order for order in self.order_book if order.ticker == ticker]
        history_book = [order for order in self.orders_history if
                      order.ticker == ticker and order.status == Status.FILLED]

        bid = max((order.price for order in order_book if order.operation == "BUY"), default=None)
        ask = min((order.price for order in order_book if order.operation == "SELL"), default=None)
        last = history_book[-1].price

        return {
            "bid": bid,
            "ask": ask,
            "last": last
        }

    def get_orders(self):
        return self.orders_history