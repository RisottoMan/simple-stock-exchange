from server import Server


class Client:
    """Client instance for sending requests to the server"""
    def __init__(self, server):
        self.server = server

    def send(self, command):
        """Send a request"""
        response = self.server.handle(command)
        return response


def main():
    """Client Application"""
    server = Server()
    client = Client(server)

    while True:
        command = input("Action: ")
        if command == "QUIT":
            break

        result = client.send(command)
        print(result, "\n")


if __name__ == "__main__":
    main()