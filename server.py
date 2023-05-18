import socket
import subprocess
import helper
import os

# AF_INET defines the socket to be for internet communication
# (as opposed to bluetooth or something)
# SOCK_STREAM means it is a stream based socket;
# connection oriented using TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ipv4_address = helper.get_non_loopback_ip()
print("IP Address: ", ipv4_address)

ports = helper.known_ports()
print("Attempting commonly open ports... ")
bound = False


def client_server_flow():
    server.listen()

    client, addr = server.accept()

    done = False

    while not done:
        msg = client.recv(1024).decode('utf-8')
        if msg == 'quit' or msg == '':
            done = True
        else:
            print("[Client]", msg)
        client.send(input("[Me] ").encode('utf-8'))

    client.close()
    server.close()


def kill_and_bind(port_to_attempt):
    subprocess.run(["bash", "kill.sh", str(port_to_attempt)])
    server.bind((ipv4_address, port_to_attempt))
    print("Running server on port", port_to_attempt, "!")
    print("IP: ", ipv4_address, "  Port: ", port_to_attempt)


for port in ports:
    try:
        if helper.validate_port(port):
            kill_and_bind(port)
            bound = True
            break
        else:
            pass
    except Exception as e:
        pass

if not bound:
    print("Failed. Analyzing processes... ")
    last_resort_ports = helper.extract_port_numbers(ipv4_address)
    for port in last_resort_ports:
        try:
            if helper.validate_port(port):
                kill_and_bind(port)
                bound = True
                client_server_flow()
                break
            else:
                pass
        except Exception as e:
            pass
else:
    client_server_flow()


