from manager import Manager
from exchange import Exchange


class Server:
    """Server for processing client requests"""
    def __init__(self):
        self.manager = Manager(self)
        self.exchange = Exchange(self)

    def handle(self, command: str):
        """Request handler"""
        parts = command.strip().upper().split()
        if not parts:
            return "EMPTY COMMAND"

        cmd = parts[0]

        if cmd == "BUY" or cmd == "SELL":
            return self.manager.create_order(*parts)

        if parts[0] == "VIEW" and parts[1] == "ORDERS":
            return self.manager.view_orders()

        if cmd == "QUOTE":
            return self.manager.get_quote(parts[1])

        return "UNKNOWN COMMAND"