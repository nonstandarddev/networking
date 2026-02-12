import socket
import click


@click.command()
@click.option("--port", default=50001, help="Desired destination port (defaults to '80' i.e. non-secure HTTP traffic)")
def main(
    port: int,
    host: str = "",
    acknowledgement: str = "Acknowledged.",
    encoding: str = "ISO-8859-1",
    socket_address_family = socket.AF_INET,
    socket_type = socket.SOCK_STREAM
):
    """
    A simple web server program.

    Note that:

    * `socket.AF_INET` indicates that we will use IPv4 addresses to communicate
    * `socket.SOCK_STREAM` indicates that we will be using TCP (`SOCK_DGRAM` indicates UDP)
    """
    http: str = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/plain\r\n"
        f"Content-Length: {len(acknowledgement)}\r\n"
        "Connection: close\r\n"
        "\r\n"
        f"{acknowledgement}"
        "\r\n\r\n"
    )
    encoded = http.encode(encoding)

    # 1. Create a new socket
    with socket.socket(socket_address_family, socket_type) as s:

        # 2. Configure options
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # 3. 'Bind' the socket to a specific port & IP 
        s.bind((host, port))

        # 4. 'Serve' the socket (i.e. make the socket available to inbound requests)
        s.listen()
        print(f"Listening on: Host ({host}), Port ({port})...")

        # 5. Create an infinite loop
        while True:

            # 6. Return a new socket once 'accepted'
            s_new, s_addr = s.accept()
            print("Connected by: ", s_addr)

            # 7. With new socket, receive data and send it back to the client
            with s_new:
                req = s_new.recv(4096)
                print("\r\n\r\n---- HTTP (Request Data) ----\r\n\r\n", req.decode(encoding=encoding, errors="ignore"))
                s_new.sendall(encoded)


if __name__ == "__main__":
    main()
