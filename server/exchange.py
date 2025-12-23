from data.order import Order


class Exchange:
    def __init__(self, server):
        self.server = server
        self.orders = []

    def create_new_order(self, operation, ticker, order_type, price, quantity) -> bool:
        pass

    def get_quote_info(self, ticker) -> str:
        pass

    def get_orders(self) -> str:
        pass