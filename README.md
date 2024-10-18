# SocketShare

SocketShare is a Python application that facilitates file sharing over a network using a client-server model. With a user-friendly GUI built using Tkinter, this application allows users to share files and folders seamlessly between connected devices.

## Features

- **User-friendly Interface**: A simple and intuitive GUI for selecting and sending files or folders.
- **Real-time Feedback**: Displays the status of the file transfer and destination details.
- **Confirmation Dialogs**: Users are prompted to confirm file reception, ensuring that files are sent only with consent.
- **Folder Compression**: Automatically compresses folders into ZIP format before transfer, simplifying the sharing process.

## Project Screenshot
![SocketShare GUI](https://i.imgur.com/Ux0GSUv.png)

## How It Works

SocketShare operates as a client-server application:

- The **Server** component listens for incoming file transfers and manages the reception of files.
- The **Client** component allows users to select files or folders to send to the server.

### Client-Server Communication

1. The client connects to the server using its IP address and a specified port.
2. The selected file or folder is sent over the TCP protocol.
3. The server confirms receipt and saves the file locally, prompting the user for confirmation if the file already exists.

## Getting Started

### Prerequisites

Before running the application, ensure that:

- **Python** is installed on your computer. [Download Python](https://www.python.org/downloads).
- The necessary libraries are included with Python, particularly Tkinter and Socket.

### Setup Instructions

1. **Update Server Configuration**:
   - In `keys.py`, set the `SERVER_HOST` variable to the IP address of the computer running the server.
   - Ensure the `SERVER_PORT` is the same on both server and client.

   ```python
    class Keys:
        # Change this to the IP of the computer running the server
        SERVER_HOST = '192.168.x.x'    # You can find by typing IPCONFIG command at ipv4
        SERVER_PORT = 1999             # Ensure this matches the server port
    ```

2. **Running the Server**:
   - Navigate to the project directory and execute the `setup_server.py` script. This script initializes the server.

   ```python
   server = Server('192.168.x.x', 1999, root) # Change this to the IP of the computer that is receiving the files

   ```

3. **Running the Client**:
   - In a separate terminal or command prompt, run the `main.py` script to start the client interface.

### Notes for Multiple Computers

- Each computer running the application must have the correct IP address set in the `keys.py` file. Make sure the `SERVER_HOST` reflects the actual IP of the machine hosting the server.
- When transferring files between virtual machines and a real computer, ensure that both machines are on the same network and can communicate with each other. You may need to adjust firewall settings to allow connections on the specified port (default: 1999).

### Example Use Case

1. Start the server on a machine (`192.168.x.x`).
2. Update the `SERVER_HOST` in the client code to point to the server's IP.
3. Select a file or folder in the client interface and initiate the transfer.
4. The server will receive the file and prompt for confirmation before saving it.

## Limitations

- The current implementation is designed for use within a local network. While it can be configured for broader use, such as over the internet, additional security and networking considerations would need to be addressed.

## Future Enhancements

- Expand functionality to support multiple simultaneous transfers.
- Implement encryption for secure file sharing over public networks.
- Enable drag-and-drop support for easier file selection.

## Conclusion

SocketShare provides an efficient and straightforward way to share files over a local network, combining ease of use with essential functionality. Modify the server settings to tailor it to your environment, and enjoy seamless file transfers!
