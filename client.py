import sys
from socket import *
import time

def serverThread(clientSocket: socket):
    """
    Function to monitor the server separately from monitoring stdin
    """
    return
def main():
    args = sys.argv
    HOST = args[1]
    PORT = int(args[2])
    password = args[3]
    name = args[4]
    print(f"Connecting to to {HOST} on port {PORT}...\n")
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((HOST, PORT))
    clientSocket.send(f"{password}\n".encode())
    time.sleep(10)
    clientSocket.send(f"{name}\n".encode())
    welcomeMessage = clientSocket.recv(1024)
    print(welcomeMessage.decode())


    clientSocket.close()

    

if __name__ == "__main__":
    main()
