import socket
import helper

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverIP = str(input("Server IP: "))
port = int(input("Port: "))

client.connect((serverIP, port))

done = False

while not done:
    client.send(input("[Me] ").encode('utf-8'))
    msg = client.recv(1024).decode('utf-8')
    if msg == 'quit':
        done = True
    else:
        print("[Server]", msg)

client.close()