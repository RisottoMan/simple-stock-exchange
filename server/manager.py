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

        if order_type == "LMT" and len(parts) == 4:
            return "INVALID NUMBER ARGUMENTS FOR ORDER TYPE"

        #todo - попытаться проверить, что quantity это целое число
        self.server.exchange.create_order(ticker, operation, order_type, price, int(quantity))

        if order_type == "LMT":
            return f"You have placed a limit {operation.lower()} order for {quantity} {ticker} shares at ${float(price):.2f} each."
        else:
            return f"You have placed a market order for {quantity} {ticker} shares."

    def get_quote(self, ticker) -> str:
        """Get information about quotes"""
        if ticker is None or ticker == "":
            return "EMPTY TICKER ARGUMENT"

        quote = self.server.exchange.get_quote(ticker)
        if quote is None:
            return "INCORRECT TICKER NAME"

        return f"{ticker} BID: ${quote["bid"]:.2f} ASK: ${quote["ask"]:.2f} LAST: ${quote["last"]:.2f}"

    def view_orders(self) -> str:
        """Show all orders"""
        orders = self.server.exchange.get_orders()

        result_lines = []
        for i, order in enumerate(orders, start=1):
            result_lines.append(f"{i}. {order}")
        return "\n".join(result_lines)