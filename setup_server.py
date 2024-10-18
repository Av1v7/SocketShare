import socket
import threading
import tkinter as tk
from utils import Utils
from tkinter import messagebox, scrolledtext
import os

SCREEN_WIDTH = 550
SCREEN_HEIGHT = 350

class Server:
    def __init__(self, host, port, root):
        self.host = host
        self.port = port
        self.root = root
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        self.setup_ui()
        self.running = True

    def setup_ui(self):
        self.root.title("File Transfer Server")
        self.root.resizable(False, False)
        Utils.center_screen(self.root, SCREEN_WIDTH, SCREEN_HEIGHT)

        title_label = tk.Label(self.root, text="File Transfer Server", font=("Helvetica", 16))
        title_label.pack(pady=10)

        self.status_label = tk.Label(self.root, text="Waiting for files...", font=("Helvetica", 12))
        self.status_label.pack(pady=5)

        self.log_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=10, font=("Helvetica", 10))
        self.log_area.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

        close_button = tk.Button(self.root, text="Close Server", command=self.close_server, bg="red", fg="white", width=100, height=110)
        close_button.pack(pady=10)

    def start_server(self):
        self.log("Server started on {}:{}".format(self.host, self.port))
        while self.running:
            client_socket, client_address = self.server_socket.accept()
            self.log(f"Connection from {client_address}")
            threading.Thread(target=self.handle_tcp_client, args=(client_socket, client_address)).start()

    def handle_tcp_client(self, client_socket, client_address):
        try:
            file_name = self.receive_data(client_socket).decode()
            client_socket.send(b"ACK")
            file_size = int(self.receive_data(client_socket).decode())
            client_socket.send(b"ACK")

            file_path = os.path.join(os.getcwd(), file_name)

            self.confirm_file_receive(client_socket, file_name, file_path, file_size, client_address)
        except Exception as e:
            self.log(f"Error handling client: {e}")
        finally:
            client_socket.close()

    def confirm_file_receive(self, client_socket, file_name, file_path, file_size, client_address):
        if os.path.exists(file_path):
            overwrite = messagebox.askyesno("File Exists", f"The file '{file_name}' already exists. Do you want to overwrite it?")
            if not overwrite:
                self.log(f"File '{file_name}' from {client_address[0]} was rejected.")
                return
        
        root = tk.Tk()
        root.withdraw()
        confirm = messagebox.askyesno("File Received", f"You are about to receive a file named '{file_name}' ({file_size} bytes) from {client_address[0]}. Do you want to accept it?")
        root.destroy()
        
        if confirm:
            self.receive_file(client_socket, file_path, file_size)
            self.save_and_show_message(client_address, file_path)
        else:
            self.log(f"File '{file_name}' from {client_address[0]} was rejected.")

    def receive_data(self, client_socket):
        data = b''
        while True:
            chunk = client_socket.recv(1024)
            data += chunk
            if len(chunk) < 1024:
                break
        return data

    def receive_file(self, client_socket, file_path, file_size):
        with open(file_path, "wb") as f:
            received_size = 0
            while received_size < file_size:
                data = client_socket.recv(min(4096, file_size - received_size))
                if not data:
                    break
                f.write(data)
                received_size += len(data)
            
            print(f"Received {received_size} bytes out of {file_size} bytes.")

    def save_and_show_message(self, client_address, file_path):
        message = f"You received data from {client_address[0]}:\n{file_path}"
        self.log(message)
        messagebox.showinfo("Data Received", message)

    def log(self, message):
        """Log messages to the log area."""
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.yview(tk.END)

    def close_server(self):
        """Close the server and exit."""
        self.running = False
        self.server_socket.close()
        self.log("Server closed.")
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    server = Server('192.168.x.x', 1999, root) # The IP of the computer that is receiving the files
    threading.Thread(target=server.start_server).start()

    root.mainloop()
