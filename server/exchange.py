from .data import Order
from .enum import Status, Operation, OrderType


class Exchange:
    def __init__(self, server):
        self.server = server
        self.orders_history = []
        self.order_book = []

    def create_order(self, ticker, operation, order_type, price, quantity) -> bool:
        try:
            order = Order(ticker, operation, order_type, price, quantity)
        except:
            return False

        self.orders_history.append(order)
        self.__execute_order(order)
        return True

    def __execute_order(self, order: Order) -> None:
        operation = Operation.BUY if order.operation == Operation.SELL else Operation.SELL
        is_reverse = (operation == Operation.BUY)
        filtered_order_book = filter(lambda item: item.ticker == order.ticker
                                     and item.operation == operation, self.order_book)

        for order_item in sorted(filtered_order_book, key=lambda value: value.price, reverse=is_reverse):
            if order.quantity == order.filled_quantity:
                break

            if order.order_type == OrderType.LIMIT:
                if order.operation == Operation.BUY and order_item.price > order.price:
                    break
                if order.operation == Operation.SELL and order_item.price < order.price:
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

            if order.order_type == OrderType.LIMIT:
                self.order_book.append(order)

    def get_quote(self, ticker) -> dict:
        order_book = [order for order in self.order_book if order.ticker == ticker]
        history_book = [order for order in self.orders_history if
                      order.ticker == ticker and order.status == Status.FILLED]

        bid = max((order.price for order in order_book if order.operation == Operation.BUY), default=None)
        ask = min((order.price for order in order_book if order.operation == Operation.SELL), default=None)
        last = history_book[-1].price

        return {
            "bid": bid,
            "ask": ask,
            "last": last
        }

    def get_orders(self) -> list:
        return self.orders_history