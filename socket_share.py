from tkinter import filedialog, ttk
import tkinter as tk
import os
import threading
import socket
import shutil
from utils import Utils

SCREEN_WIDTH = 550
SCREEN_HEIGHT = 350

class SocketShare:
    def __init__(self, root, server_host, server_port) -> None:
        self.root = root
        self.server_host = server_host
        self.server_port = server_port
        self.file_to_share = None

        self.setup_ui()

    def setup_ui(self):
        self.root.title("Socket Share")
        self.root.resizable(False, False)
        Utils.center_screen(self.root, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True, fill=tk.BOTH)

        title_label = ttk.Label(frame, text="Socket Share", font=("Helvetica", 18, "bold"))
        title_label.pack(pady=(0, 10))

        instruction_label = ttk.Label(frame, text="Select a file or folder to share:", font=("Helvetica", 12))
        instruction_label.pack(pady=(0, 5))

        self.file_label = ttk.Label(frame, text="No file selected", width=50, relief=tk.SUNKEN, anchor="w")
        self.file_label.pack(pady=(0, 10))

        self.browse_button = ttk.Button(frame, text="Browse File/Folder", command=self.browse_file)
        self.browse_button.pack(pady=(0, 10))

        self.send_button = ttk.Button(frame, text="Send", command=self.share_data)
        self.send_button.pack(pady=(0, 10))

        self.dest_label = ttk.Label(frame, text="Sending to: N/A", font=("Helvetica", 10))
        self.dest_label.pack(pady=(10, 0))

        style = ttk.Style()
        style.configure("Accent.TButton", font=("Helvetica", 12))
        self.browse_button.config(style="Accent.TButton")
        self.send_button.config(style="Accent.TButton")

    def browse_file(self):
        self.file_to_share = filedialog.askopenfilename()
        if self.file_to_share:
            self.file_label.config(text=os.path.basename(self.file_to_share))

    def share_data(self):
        if self.file_to_share:
            self.send_file()

    def send_file(self):
        print(f"Sending file: {self.file_to_share}")
        self.update_destination_label()
        threading.Thread(target=self.send_data, args=(self.file_to_share,)).start()

    def send_data(self, data):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.server_host, self.server_port))

        if os.path.isfile(data):
            self.send_single_file(client_socket, data)
        elif os.path.isdir(data):
            self.send_folder(client_socket, data)
        else:
            print("Data is not a valid file or directory")

        client_socket.close()

    def send_single_file(self, client_socket, file_path):
        file_name = os.path.basename(file_path)
        with open(file_path, 'rb') as f:
            file_data = f.read()

        client_socket.sendall(file_name.encode())
        client_socket.recv(1024)

        file_size = len(file_data)
        client_socket.sendall(str(file_size).encode())
        client_socket.recv(1024)

        client_socket.sendall(file_data)

    def send_folder(self, client_socket, folder_path):
        zip_path = shutil.make_archive(folder_path, 'zip', folder_path)
        self.send_single_file(client_socket, zip_path)
        
        os.remove(zip_path)

    def update_destination_label(self):
        self.dest_label.config(text=f"Sending to: {self.server_host}:{self.server_port}")