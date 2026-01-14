from server import Server


def main():
    """Client Application"""
    server = Server()

    while True:
        command = input("Action: ")
        if command == "QUIT":
            break

        result = server.handle(command)
        print(result, "\n")


if __name__ == "__main__":
    main()