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


@click.command()
@click.option("--port", default=28333, help="Desired destination port (defaults to '80' i.e. non-secure HTTP traffic)")
def main(
    port: int,
    host: str = "",
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

    with socket.socket(socket_address_family, socket_type) as s:

        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        print(f"Listening on: Host ({"localhost" if not host else host}), Port ({port})...")

        while True:

            s_new, s_addr = s.accept()
            print("Connected by: ", s_addr)

            with s_new:

                buffer = b""
                while b"\r\n\r\n" not in buffer:
                    chunk = s_new.recv(4096)
                    if not chunk:
                        break
                    buffer += chunk
                
                decoded = buffer.decode(encoding=encoding, errors="ignore")
                lines = decoded.split("\r\n")

                request_header = lines[0]
                request_header_components = request_header.split(" ")

                # a) Parse request header item (to get the file path)
                request_method = request_header_components[0]
                request_path = request_header_components[1]
                request_protocol = request_header_components[2]

                # b) Strip the path off (for security reasons)
                request_file = request_path.split("/")[-1]

                # c) Determine file type
                try:
                    extension = os.path.splitext(request_file)[1]
                    content_type = MIME_TYPES[extension]
                except KeyError:
                    print(f"File with extension '{extension}' not supported by this web server")
                    encoded = HTTP_404.encode(encoding)
                    s_new.sendall(encoded)
                    continue

                # d) Read the data from the named file
                try:
                    with open(os.path.join("resources", request_file), "rb") as fp:
                        content = fp.read() 
                except FileNotFoundError:
                    print(f"Requested resource '{request_file}' cannot be found on this web server")
                    encoded = HTTP_404.encode(encoding)
                    s_new.sendall(encoded)
                    continue

                # e) Build HTTP response packet
                http: str = (
                    "HTTP/1.1 200 OK\r\n"
                    f"Content-Type: {content_type}\r\n"
                    f"Content-Length: {len(content)}\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                    f"{content}"
                    "\r\n\r\n"
                )
                encoded = http.encode(encoding)

                # d) Issue HTTP response packet to the client
                s_new.sendall(encoded)


if __name__ == "__main__":
    main()
