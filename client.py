import sys
from socket import *
import time
import threading

def serverThread(clientSocket: socket):
    """
    Function to monitor incoming server messages separately from monitoring stdin
    """
    return
def main():
    args = sys.argv
    HOST = args[1]
    PORT = int(args[2])
    password = args[3]
    name = args[4]
    print(f"Connecting to {HOST} on port {PORT}...")
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((HOST, PORT))
    clientSocket.send(f"{password}".encode())
    time.sleep(1)
    clientSocket.send(f"{name}".encode())
    welcomeMessage = clientSocket.recv(1024)
    print(welcomeMessage.decode())
    serverMonitor = threading.Thread(target=serverThread, 
                                            args = ())
    serverMonitor.daemon = True
    serverMonitor.start()
    clientSocket.close()
    #while True:
        #time.sleep(1)


    

if __name__ == "__main__":
    main()
