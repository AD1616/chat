import tkinter as tk
import socket

global serverIP
global port


def submit():
    serverIP = str(entry1.get())
    port = int(entry2.get())
    result_label.config(text="IP: " + serverIP + "\nPort: " + str(port))

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect((serverIP, port))

    text_box = tk.Text(root, width=50, height=10)
    text_box.pack()

    input_entry = tk.Entry(root, width=50)
    input_entry.pack()



    def message():
        data = input_entry.get()
        send(data)

    def send(data):
        client.send(data.encode('utf-8'))
        input_entry.delete(0, tk.END)
        msg = client.recv(1024).decode('utf-8')
        if msg == 'quit':
            client.close()
        else:
            populate_text("[Server]" + msg + "\n")
            print("[Server]", msg)

    submit_button = tk.Button(root, text="Submit", command=message)
    submit_button.pack()

    def populate_text(data):
        text_box.insert(tk.END, data)

    # done = False

    # while not done:
        #client.send(input("[Me] ").encode('utf-8'))
        # msg = client.recv(1024).decode('utf-8')
        # if msg == 'quit':
        #     done = True
        # else:
        #     populate_text("[Server]" + msg + "\n")
        #     print("[Server]", msg)

    # client.close()


# Create a Tkinter window
root = tk.Tk()
root.title("Chat Client")

# Create the first input box
label1 = tk.Label(root, text="IP:")
label1.pack()

entry1 = tk.Entry(root, width=50)
entry1.pack()

# Create the second input box
label2 = tk.Label(root, text="Port:")
label2.pack()

entry2 = tk.Entry(root, width=50)
entry2.pack()

# Create the submit button
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.pack()

# Create the result label
result_label = tk.Label(root, text="")
result_label.pack()



# Start the GUI main loop
root.mainloop()
