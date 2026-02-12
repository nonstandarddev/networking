import socket
import click


@click.command()
@click.option("--host", default="example.com", help="Desired host / website (e.g. 'example.com')")
@click.option("--port", default=80, help="Desired destination port (defaults to '80' i.e. non-secure HTTP traffic)")
def main(
    host: str,
    port: int,
    encoding: str = "ISO-8859-1",
    socket_address_family = socket.AF_INET,
    socket_type = socket.SOCK_STREAM
):
    """
    A simple web client program.

    Note that:

    * `socket.AF_INET` indicates that we will use IPv4 addresses to communicate
    * `socket.SOCK_STREAM` indicates that we will be using TCP (`SOCK_DGRAM` indicates UDP)
    """

    http: str = (
        "GET / HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        "Connection: close\r\n"
        "\r\n"
    )
    encoded = http.encode(encoding)

    with socket.socket(socket_address_family, socket_type) as s:
        s.connect((host, port))
        s.sendall(encoded)
        response = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk
    
    decoded = response.decode(encoding, errors="ignore")

    print(decoded)


if __name__ == "__main__":
    main()
