"""
A simple web server program built in Python.

To administer this server simply run,

```
uv run webserver.py
```

This web server (by default) exposes itself to inbound connections on port 28333.

You can modify the server parameters by providing command-line arguments. For instance,

```
uv run webserver.py --port=8081
```
"""
import socket
import click
import os


MIME_TYPES: dict[str, str] = {
    ".txt": "text/plain",
    ".html": "text/html"
}


HTTP_404: str = (
    "HTTP/1.1 404 Not Found\r\n"
    "Content-Type: text/plain\r\n"
    "Content-Length: 13\r\n"
    "Connection: close\r\n"
    "\r\n"
    "404 not found"
    "\r\n\r\n"
)


class WebServer:

    def __init__(
        self, 
        host: str = "",
        port: int = 28333, 
        encoding: str = "ISO-8859-1"
    ):
        self.host = host
        self.port = port
        self.encoding = encoding

    def expose(self):
        """
        Expose web server to incoming connections.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.listen()
            print(f"Listening on {self.host or 'localhost'}:{self.port}")

            while True:
                conn, addr = s.accept()
                print("Connected by:", addr)
                with conn:
                    self.handle_connection(conn)

    def handle_connection(self, conn):
        request = self.read_request(conn)
        if not request:
            return

        method, path, protocol = self.parse_request_line(request)
        filename = path.split("/")[-1]

        response = self.build_response(filename)
        conn.sendall(response)

    def read_request(self, conn):
        buffer = b""
        while b"\r\n\r\n" not in buffer:
            chunk = conn.recv(4096)
            if not chunk:
                break
            buffer += chunk
        return buffer.decode(self.encoding, errors="ignore")

    def parse_request_line(self, request):
        first_line = request.split("\r\n")[0]
        return first_line.split(" ")

    def build_response(self, filename):
        extension = os.path.splitext(filename)[1]

        if extension not in MIME_TYPES:
            return HTTP_404.encode(self.encoding)

        try:
            with open(os.path.join("resources", filename), "rb") as fp:
                content = fp.read()
        except FileNotFoundError:
            return HTTP_404.encode(self.encoding)

        headers = (
            "HTTP/1.1 200 OK\r\n"
            f"Content-Type: {MIME_TYPES[extension]}\r\n"
            f"Content-Length: {len(content)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )

        return headers.encode(self.encoding) + content + b"\r\n\r\n"



@click.command()
@click.option("--port", default=28333, help="Desired destination port (defaults to '80' i.e. non-secure HTTP traffic)")
def main(
    port: int,
    host: str = "",
    encoding: str = "ISO-8859-1"
):
    """
    A simple web server CLI.
    """
    ws = WebServer(
        host,
        port,
        encoding
    )
    ws.expose()


if __name__ == "__main__":
    main()
