from client.client import Client
from server.server import Server


def main():
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