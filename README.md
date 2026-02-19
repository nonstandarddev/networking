# Networking (with Python!) :satellite:

This repository is dedicated to spreading knowledge about TCP / IP and, more generally, how
inter-network communication works 'under the hood'.

It is informed by Beej's "Guide to Networking" which can be found [here](https://beej.us/guide/).

# Usage

## Setup :toolbox:

To setup this repository using `uv`, simply type,

```
uv sync
```

## Web Server

Once setup is complete you can administer a simple web server as follows,

```
uv run webserver.py
```

This web server (by default) exposes itself to inbound connections on port `28333`.

You can modify the server parameters by providing command-line arguments. For instance, the following
command will administer the server on port `8081`

```
uv run webserver.py --port=8081
```

## Web Client

To administer the client, simply run,

```
uv run webclient.py
```

This web client (by default) will issue a HTTPS request to the website `example.com`

But you can also query your own local web server - assuming the defaults are used - as follows,

```
uv run webclient.py --host="127.0.0.1" --port=28333
```