class Client:
    """Client for sending requests to the server"""
    def __init__(self, server):
        self.server = server

    def send(self, command):
        """Send a request"""
        response = self.server.handle(command)
        return response