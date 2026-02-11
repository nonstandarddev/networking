import socket
import click


@click.command()
@click.option("--host", default="example.com", help="Desired host / website (e.g. 'example.com')")
@click.option("--port", default=80, help="Desired destination port (defaults to '80' i.e. non-secure HTTP traffic)")
def main(
    host: str,
    port: int,
    encoding: str = "ISO-8859-1"
):
    
    http: str = (
        f"GET / HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    )
    encoded = http.encode(encoding)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
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
    
    return decoded


if __name__ == "__main__":
    main()
