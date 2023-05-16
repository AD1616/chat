# Chat

The goal of this project is for two computers to be able to communicate using the TCP/IP protocol over a restricted network.

"Restricted" means that the network blocks connections over some ports. As such, we take advantage of the loop hole that an established connection on a port must be one that is allowed by the router.

We mount our server on a port previously used by an unwanted process.

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

### Start Client

#### Command Line

```shell
python client.py
```

Enter the IP/Port that the server is running on. 

#### GUI

```shell
python gui_client.py
```

Enter the port that the server is running on.
