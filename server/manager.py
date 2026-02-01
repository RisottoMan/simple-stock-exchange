from .enum import Operation, OrderType, ServerMessage


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
            return ServerMessage.INVALID_COMMAND

        if operation not in Operation:
            return ServerMessage.INVALID_OPERATION

        if order_type not in OrderType:
            return ServerMessage.INVALID_ORDER_TYPE

        if order_type == OrderType.LIMIT and len(parts) == 4:
            return ServerMessage.INVALID_ORDER_TYPE_ARGUMENTS

        response = self.server.exchange.create_order(ticker, operation, order_type, price, int(quantity))
        if not response:
            return ServerMessage.ORDER_CREATE_ERROR

        if order_type == OrderType.LIMIT:
            return f"You have placed a limit {operation.lower()} order for {quantity} {ticker} shares at ${float(price):.2f} each."
        else:
            return f"You have placed a market order for {quantity} {ticker} shares."

    def get_quote(self, ticker) -> str:
        """Get information about quotes"""
        if ticker is None or ticker == "":
            return ServerMessage.EMPTY_TICKER_ARGUMENT

        quote = self.server.exchange.get_quote(ticker)
        if quote is None:
            return ServerMessage.INCORRECT_TICKER_NAME

        return f"{ticker} BID: ${quote["bid"]:.2f} ASK: ${quote["ask"]:.2f} LAST: ${quote["last"]:.2f}"

    def view_orders(self) -> str:
        """Show all orders"""
        orders = self.server.exchange.get_orders()

        result_lines = []
        for i, order in enumerate(orders, start=1):
            result_lines.append(f"{i}. {order}")
        return "\n".join(result_lines)