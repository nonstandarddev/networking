"""
To administer this client, simply run,

```
uv run webclient.py
```

This web client (by default) will issue a HTTPS request to the website `example.com`

But you can also query your own local web server - assuming the defaults are used - as follows,

```
uv run webclient.py --host="127.0.0.1" --port=28333
```
"""
import socket
import click


class WebClient:

    def __init__(
        self,
        host: str,
        port: int,
        resource: str,
        encoding: str
    ):
        self.host = host
        self.port = port
        self.resource = resource
        self.encoding = encoding
    
    def issue_request(self):
        encoded = self.build_request()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(encoded)
            response = self.read_response(s)
        print(response)

    def build_request(self) -> str:
        http: str = (
            f"GET {self.resource} HTTP/1.1\r\n"
            f"Host: {self.host}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )
        return http.encode(self.encoding)

    def read_response(self, conn) -> str:
        buffer = b""
        while True:
            chunk = conn.recv(4096)
            if not chunk:
                break
            buffer += chunk
        return buffer.decode(self.encoding, errors="ignore")


@click.command()
@click.option("--host", default="example.com", help="Desired host / website (e.g. 'example.com')")
@click.option("--port", default=80, help="Desired destination port (defaults to '80' i.e. non-secure HTTP traffic)")
@click.option("--resource", default="/", help="Desired resource on the destination server")
def main(
    host: str,
    port: int,
    resource: str,
    encoding: str = "ISO-8859-1"
):
    """
    A simple web client CLI.
    """
    wc = WebClient(
        host,
        port,
        resource,
        encoding
    )
    wc.issue_request()


if __name__ == "__main__":
    main()
