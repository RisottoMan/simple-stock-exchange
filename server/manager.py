class Manager:
    def __init__(self, server):
        self.server = server

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

        self.server.exchange.create_new_order(operation, ticker, order_type, price, quantity)

        if order_type == "LMT":
            return f"You have placed a limit {operation.lower()} order for {quantity} {ticker} shares at ${float(price):.2f} each."
        else:
            return f"You have placed a market order for {quantity} {ticker} shares."

    def get_quote(self, ticker) -> str:
        """Get information about quotes"""
        quote = self.server.exchange.get_quote_info(ticker)
        return f"{quote.name} BID: ${quote.bid} ASK: ${quote.ask} LAST: ${quote.last}"

    def view_orders(self) -> str:
        """Show all orders"""
        orders = self.server.exchange.get_orders()

        result_lines = []
        for i, order in enumerate(orders, start=1):
            result_lines.append(f"{i}. {order}")
        return "\n".join(result_lines)