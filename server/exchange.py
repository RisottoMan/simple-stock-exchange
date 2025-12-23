from server.data.order import Order


class Exchange:
    def __init__(self, server):
        self.server = server
        self.orders = []
        self.order_book = {
            "SNAP":
                {
                    "BUY": [
                        {"price": 29.00, "quantity": 100},
                        {"price": 30.00, "quantity": 20},
                        {"price": 30.50, "quantity": 10},
                    ],
                    "SELL": [
                        {"price": 31.00, "quantity": 34},
                        {"price": 31.50, "quantity": 23},
                        {"price": 32.00, "quantity": 100},
                    ],
            },
            "FB":
                {
                    "BUY": [{"price": 25.00, "quantity": 100}],
                    "SELL": [{"price": 26.00, "quantity": 50}],
            }
        }
        self.last_price = {
            "SNAP": 30.00,
            "FB": 26.00
        }

    def create_order(self, operation, ticker, order_type, price, quantity):
        order = Order(operation, ticker, order_type, price, quantity)
        self.orders.append(order)

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
        return self.orders