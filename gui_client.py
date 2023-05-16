import tkinter as tk
import socket
import threading
import helper

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

closing = False


def submit():
    ip = helper.get_non_loopback_ip()
    port = int(port_input.get())
    result_label.config(text="IP: " + ip + "\nPort: " + str(port))

    client.connect((ip, port))

    label_port_input.destroy()
    port_input.destroy()
    submit_button.destroy()

    text_box = tk.Text(root, width=50, height=10, state="disabled", highlightcolor="red", highlightthickness=2)
    text_box.pack()

    frame = tk.Frame(root)
    frame.pack()

    space = tk.Label(frame, height=1)
    space.pack()

    input_message_to_send = tk.Entry(root, width=35)
    input_message_to_send.pack()

    def receive_message():
        while not closing:
            incoming_message = client.recv(1024).decode('utf-8')
            input_message_to_send.config(state="normal")
            input_message_to_send.pack()
            if incoming_message == 'quit':
                client.close()
                break
            else:
                populate_text("[Server]" + incoming_message + "\n")

    def send_message(event=None):
        data = input_message_to_send.get()
        if data != "":
            populate_text("[Me]" + data + "\n")
            input_message_to_send.delete(0, tk.END)
            client.send(data.encode('utf-8'))
            input_message_to_send.pack_forget()
            input_message_to_send.config(state="disabled")

    input_message_to_send.bind("<Return>", send_message)

    receive_thread = threading.Thread(target=receive_message)
    receive_thread.start()

    def populate_text(data):
        text_box.config(state="normal")
        text_box.insert(tk.END, data)
        text_box.see(tk.END)
        text_box.config(state="disabled")


# Create a Tkinter window
root = tk.Tk()
root.title("Chat Client")

label_port_input = tk.Label(root, text="Port:", justify="center", anchor="center")
label_port_input.pack()

port_input = tk.Entry(root, width=20, justify="center")
port_input.pack()

submit_button = tk.Button(root, text="Connect", command=submit)
submit_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()


def on_closing():
    closing = True
    if client:
        client.close()  # Close the socket connection if it exists
    root.destroy()


# Start the GUI main loop
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
