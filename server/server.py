from .manager import Manager
from .enum import ServerMessage, ServerCommand


class Server:
    """Server for processing client requests"""
    def __init__(self):
        self.manager = Manager()

    def handle(self, command: str) -> str:
        """Request handler"""
        parts = command.strip().upper().split()
        if not parts:
            return ServerMessage.EMPTY_COMMAND

        cmd = parts[0]

        if cmd == ServerCommand.BUY or cmd == ServerCommand.SELL:
            return self.manager.create_order(*parts)

        if command == ServerCommand.VIEW_ORDERS:
            return self.manager.view_orders()

        if cmd == ServerCommand.QUOTE:
            return self.manager.get_quote(parts[1])

        return ServerMessage.UNKNOWN_COMMAND