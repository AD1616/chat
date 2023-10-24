# Chat

The goal of this project is to develop a chat service for communication using the TCP/IP and UDP protocols.

One version allows only one client that communicates with another client hosting the server. The other version allows for multiple clients to connect to a non-client server.

The TCP/IP protocol is used for messaging between the client and server. The UDP protocol is used for device discovery, allowing a server to communicate its IP and port to a client without a previously established connection.

## Installation
```shell
git clone https://github.com/AD1616/chat.git
```

```shell
cd chat
```

```shell
pip install -r requirements.txt
```
## One Client

### Start Server

```shell
python server.py
```

### Start GUI Client

```shell
python gui_client.py
```

## Multiple Clients

### Start Server

```shell
python multi_server.py
```

### Start GUI Client

```shell
python gui_multi_client.py
```
