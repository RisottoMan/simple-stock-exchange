from .data import Order


class Exchange:
    def __init__(self, server):
        self.server = server
        self.orders = []
        self.order_book = {
            "SNAP":
                {
                    "BUY": [
                        {"price": 30.50, "quantity": 10},
                        {"price": 30.00, "quantity": 20},
                        {"price": 29.00, "quantity": 100},
                    ],
                    "SELL": [
                        {"price": 31.00, "quantity": 10},
                        {"price": 31.50, "quantity": 30},
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
        new_order = Order(operation, ticker, order_type, price, quantity)
        self.orders.append(new_order)

        temp_quantity = quantity
        book = self.order_book.get(ticker)
        current_orders = book.get("BUY" if operation == "SELL" else "SELL")

        for order in current_orders:
            if temp_quantity <= 0:
                break

            if order_type == "LMT":
                if operation == "BUY" and order["price"] > float(price):
                    break
                if operation == "SELL" and order["price"] < float(price):
                    break

            can_take = min(temp_quantity, order["quantity"])
            order["quantity"] -= can_take
            temp_quantity -= can_take
            new_order.filled_quantity += can_take
            new_order.status = "PARTIAL"

            if order["quantity"] == 0:
                current_orders.remove(order)

        if temp_quantity == 0:
            new_order.status = "FILLED"
        else:
            if order_type == "LMT":
                self.order_book[ticker][operation].append({
                    "price": float(price),
                    "quantity": temp_quantity
                })
            elif order_type == "MKT":
                new_order.status = "PARTIAL CANCELED"

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