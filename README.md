# Chat

The goal of this project is for two computers to be able to communicate using the TCP/IP and UDP protocols over a restricted network.

"Restricted" means that the network blocks connections over some ports. As such, we take advantage of the loop hole that an established connection on a port must be one that is allowed by the router (in the worst case scenario that no other generally open ports can be bound). We mount our server on a port previously used by an unwanted process.

The TCP/IP protocol is used for messaging between the client and server. The UDP protocol is used for device discovery, allowing a server to communicate its IP and port to a client without a previously established connection.

### Installation
```shell
git clone https://github.com/AD1616/chat.git
```

```shell
cd chat
```

```shell
pip install -r requirements.txt
```
### Start Server

```shell
python server.py
```
The program needs to find an established port to mount the server on. You will be asked to terminate a process to allow this.

### Start GUI Client

```shell
python gui_client.py
```
