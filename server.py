import socket
import subprocess
import time
import helper
import os
import rsa
import threading

# AF_INET defines the socket to be for internet communication
# (as opposed to bluetooth or something)
# SOCK_STREAM means it is a stream based socket;
# connection oriented using TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# We use a UDP socket to broadcast the IP and port of the server
# The client is set up to listen to the server's broadcast on a specific port
server_broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

broadcast_port = 64667
bound_port = 0

done = False

ipv4_address = helper.get_non_loopback_ip()
print("IP Address: ", ipv4_address)

ports = helper.known_ports()
print("Attempting commonly open ports... ")
bound = False


def client_server_flow():
    server.listen()

    client, addr = server.accept()
    
    # receive public key from client
    client_pubkey = eval(client.recv(1024).decode('utf-8')) # back to tuple
    print("Client public key: ", client_pubkey)
    
    # send public key to client
    pubkey, privkey = rsa.generate(10)
    client.send(str(pubkey).encode('utf-8'))
    print("Public key sent to client")

    # ******* TEST ENCRYPTION ******* 
    # test_msg = "asflsdjfls"
    # client.send(str(rsa.encrypt(test_msg, client_pubkey)).encode('utf-8'))
    # print("Encrypted message sent to client")
    # # verify client reply is correct
    # if rsa.decrypt(client.recv(1024), privkey).decode('utf-8') == test_msg:
    #     print("Test successful")
    # else:
    #     print("Test failed")
    #     return


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
    bound_port = port_to_attempt

    # Broadcast the IP and port of the server
    def broadcast_for_new_clients():
        while not done:
            message = f"Server IP address: {ipv4_address}, Port: {bound_port}"
            server_broadcast_socket.sendto(message.encode(), ("<broadcast>", broadcast_port))
            time.sleep(5)

    broadcast_thread = threading.Thread(target=broadcast_for_new_clients)
    broadcast_thread.start()

    print("Running server on port", port_to_attempt, "!")
    print("IP: ", ipv4_address, "  Port: ", port_to_attempt)


for port in ports:
    try:
        if helper.validate_port(port):
            kill_and_bind(port)
            bound = True
            break
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
        except Exception as e:
            pass
else:
    client_server_flow()


    

    