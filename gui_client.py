import tkinter as tk
import socket
import threading
import helper
import rsa

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


closing = False

# update the textbox content while keeping it
# in a disabled state for the user
def populate_text(data, text):
    text.config(state="normal")
    text.insert(tk.END, data)
    text.see(tk.END)
    text.config(state="disabled")


def submit():
    server_ip = str(ip_input.get())

    ports = helper.known_ports()

    connected = False
    for port in ports:
        try:
            client.connect((server_ip, port))
            result_label.config(text="IP: " + server_ip + "\nPort: " + str(port))
            connected = True
        except:
            pass

    if not connected:
        label_port_input = tk.Label(root, text="Port:", justify="center", anchor="center")
        label_port_input.pack()

        port_input = tk.Entry(root, width=20, justify="center")
        port_input.pack()

        port = int(port_input.get())
        client.connect((server_ip, port))

        result_label.config(text="IP: " + server_ip + "\nPort: " + str(port))

        label_port_input.destroy()
        port_input.destroy()

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
    populate_text("Server public key: " + str(server_pubkey) + "\n")

    # test decryption and send back to server
    test_msg = rsa.decrypt(client.recv(1024), privkey)
    client.send(rsa.encrypt(str(test_msg), server_pubkey))

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

    def send_message(event=None):
        data = input_message_to_send.get()
        if data != "":
            populate_text("[Me]" + data + "\n", text_box)
            input_message_to_send.delete(0, tk.END)
            client.send(data.encode('utf-8'))
            input_message_to_send.pack_forget()
            input_message_to_send.config(state="disabled")

    input_message_to_send.bind("<Return>", send_message)

    receive_thread = threading.Thread(target=receive_message)
    receive_thread.start()

# Create a Tkinter window
root = tk.Tk()
root.title("Chat Client")

text_devices = tk.Text(root, width=50, height=2, state="disabled")
text_devices.pack()

label_ip_input = tk.Label(root, text="IP:", justify="center", anchor="center")
label_ip_input.pack()

ip_input = tk.Entry(root, width=20, justify="center")
ip_input.pack()


submit_button = tk.Button(root, text="Connect", command=submit)
submit_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

client_ip = helper.get_non_loopback_ip()
devices_on_network = helper.find_devices_on_network(client_ip)
populate_text(devices_on_network, text_devices)

def on_closing():
    closing = True
    if client:
        client.close()  # Close the socket connection if it exists
    root.destroy()


# Start the GUI main loop
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
