import tkinter as tk
import socket
import threading
import helper
import rsa
import os
import sys

# TCP client to receive and send messages to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# UDP socket to receive the IP and port of the server from broadcast
client_receive_broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_receive_broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
broadcast_port = 64667
client_receive_broadcast_socket.bind(("", broadcast_port))
data, address = client_receive_broadcast_socket.recvfrom(1024)
message = data.decode()
server_ip_address = message.split(",")[0].split(":")[1].strip()
server_port = int(message.split(",")[1].split(":")[1].strip())


closing = False

# update the textbox content while keeping it
# in a disabled state for the user
def populate_text(data, text):
    text.config(state="normal")
    text.insert(tk.END, data)
    text.see(tk.END)
    text.config(state="disabled")


# flow after connection is established
def submit(event=None):
    # try to connect to broadcasted IP and port
    try:
        client.connect((server_ip_address, server_port))
    # otherwise, setup UI to allow user to enter IP and port
    except:
        label_ip_input = tk.Label(root, text="IP:", justify="center", anchor="center")
        label_ip_input.pack()

        ip_input = tk.Entry(root, width=20, justify="center")
        ip_input.pack()

        label_port_input = tk.Label(root, text="Port:", justify="center", anchor="center")
        label_port_input.pack()

        port_input = tk.Entry(root, width=20, justify="center")
        port_input.pack()

        server_ip = str(ip_input.get())
        port = int(port_input.get())

        connected = False

        try:
            port = int(port_input.get())
            client.connect((server_ip, port))
            connected = True
        except:
            pass

        label_port_input.destroy()
        port_input.destroy()

        result_label.config(text="IP: " + server_ip + "\nPort: " + str(port))

        if not connected:
            pass

        label_ip_input.destroy()
        ip_input.destroy()

    text_devices.destroy()  
    submit_button.destroy()


    text_box = tk.Text(root, width=50, height=10, state="disabled", highlightcolor="red", highlightthickness=2)
    text_box.pack()

    frame = tk.Frame(root)
    frame.pack()

    space = tk.Label(frame, height=1)
    space.pack()

    input_message_to_send = tk.Entry(root, width=35)
    input_message_to_send.pack()
    
    # send public key to server
    pubkey, privkey = rsa.generate(10)
    client.send(str(pubkey).encode('utf-8'))
    populate_text("Public key sent to server\n", text_box)
    
    # receive public key from server
    server_pubkey = eval(client.recv(1024).decode('utf-8'))
    populate_text("Server public key: " + str(server_pubkey) + "\n", text_box)

    # ******* TEST DECRYPTION ******* 
    # test_msg = rsa.decrypt(client.recv(1024), privkey)
    # client.send(rsa.encrypt(str(test_msg), server_pubkey))

    # handle incoming messages from the server
    def receive_message():
        while not closing:
            # decoded message
            incoming_message = client.recv(1024).decode('utf-8')
            # enabling textbox for client input
            input_message_to_send.config(state="normal")
            input_message_to_send.pack()
            # handle exit cases and
            # add valid message to textbox
            if incoming_message == 'quit' or '':
                client.close()
                break
            else:
                populate_text("[Server]" + incoming_message + "\n", text_box)

    # handle sending messages to the server
    def send_message(event=None):
        data = input_message_to_send.get()
        if data != "":
            populate_text("[Me]" + data + "\n", text_box)
            input_message_to_send.delete(0, tk.END)
            client.send(data.encode('utf-8'))
            # disable input box while waiting for
            # reply from server
            input_message_to_send.pack_forget()
            input_message_to_send.config(state="disabled")

    input_message_to_send.bind("<Return>", send_message)

    # start thread to receive messages
    receive_thread = threading.Thread(target=receive_message)
    receive_thread.start()

# Create a Tkinter window
root = tk.Tk()
root.title("Chat Client")

label_text_devices = tk.Label(root, text="Devices on the network: ", justify="center", anchor="center")
label_text_devices.pack()
text_devices = tk.Text(root, width=30, height=6, state="disabled")
text_devices.pack()



submit_button = tk.Button(root, text="Connect", command=submit)
submit_button.pack()


result_label = tk.Label(root, text="")
result_label.pack()

client_ip = helper.get_non_loopback_ip()


# Find all IP addresses on the network
def find_devices():
    devices_on_network = helper.find_devices_on_network(client_ip)
    message_devices = ""
    for ip in devices_on_network:
        message_devices += ip
        message_devices += "\n"
    populate_text(message_devices, text_devices)
    sys.exit()

# ********* NOT USING THIS FOR NOW *********
# find_devices_thread = threading.Thread(target=find_devices)
# find_devices_thread.start()

# Display IP and port that server broadcasted
def display_received_broadcast():
    populate_text("IP: " + str(server_ip_address) + "  Port: " + str(server_port), text_devices )
    sys.exit()

# threading to improve startup time
display_received_broadcast_thread = threading.Thread(target=display_received_broadcast)
display_received_broadcast_thread.start()

# handle closing of the window
def on_closing():
    closing = True
    if client:
        client.close()  # Close the socket connection if it exists
        os._exit(0)
    root.destroy()


# Start the GUI main loop
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
