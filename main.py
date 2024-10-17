from socket_share import SocketShare
from keys import Keys
import tkinter as tk

def main():
    server_host = Keys.SERVER_HOST
    server_port = Keys.SERVER_PORT
    
    root = tk.Tk()
    SocketShare(root, server_host, server_port)
    
    root.mainloop()

if __name__ == "__main__":
    main()
