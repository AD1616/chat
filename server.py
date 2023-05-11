import socket
import subprocess
import helper

# AF_INET defines the socket to be for internet communication
# (as opposed to bluetooth or something)
# SOCK_STREAM means it is a stream based socket;
# connection oriented using TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ipv4_address = helper.get_non_loopback_ip()
print("IP Address: ", ipv4_address)

ports = helper.extract_port_numbers(ipv4_address)
print("Trying the following available ports: ", ports)
for port in ports:
    try:
        if helper.validate_port(port):
            subprocess.run(["bash", "kill.sh", str(port)])
            server.bind((ipv4_address, port))
            print("Running server on port", port, "!")
            print("IP: ", ipv4_address, "  Port: ", port)
            break
        else:
            pass
    except Exception as e:
        pass

server.listen()

client, addr = server.accept()

done = False

while not done:
    msg = client.recv(1024).decode('utf-8')
    if msg == 'quit':
        done = True
    else:
        print(msg)
    client.send(input("Message: ").encode('utf-8'))

client.close()
server.close()