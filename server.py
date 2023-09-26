from socket import *
import threading
import sys

def clientThread(connectionSocket: socket, addr: str,
                 password: str, nameSet: set, clientDict):
    """
    operations for a single client
    """
    #check passcode
    passwordAttempt = connectionSocket.recv(1024).decode().strip()
    if passwordAttempt != password:
        #wrong password
        connectionSocket.close()
        return
    name = connectionSocket.recv(1024).decode().strip()
    if name in nameSet or " " in name:
        #name already exists or name has space  
        connectionSocket.close()
        return
    connectionSocket.send("Welcome!".encode())
    nameSet.add(name)
    joinAnnouncement = f"{name} joined the chatroom"
    #announce to all other clients that a new person has joined the chatroom
    print(joinAnnouncement, flush = True)

    #remove name from set once client leaves
    nameSet.remove(name)
    return

def main():
    args = sys.argv
    PORT = int(args[1])
    PASSWORD = args[2]
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', PORT))
    serverSocket.listen(1)
    print(f"Server started on port {PORT}. Accepting connections...\n")
    clientDict = dict() #dict of all clients. Key is client address, value is the socket object 
    threadDict = dict() #dict of all threads. Key is client address, value is the thread it is running on
    nameSet = set() #set of all names on the server
    while True:
        connectionSocket, addr = serverSocket.accept()
        clientDict[addr] = connectionSocket
        #start new thread
        threadDict[addr] = threading.Thread(target=clientThread, 
                                            args = (connectionSocket, addr, PASSWORD, nameSet, clientDict)) 
        #allows killing the thread
        threadDict[addr].daemon = True
        threadDict[addr].start()
if __name__ == "__main__":
    main()
