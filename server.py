from socket import *
import threading
import sys

def serverPrint(inStr: str):
    print(inStr, end = '', flush = False)

def clientThread(connectionSocket: socket, addr: str,
                 password: str, nameSet: set, clientDict: dict):
    """
    operations for a single client
    """
    #check passcode
    passwordAttempt = connectionSocket.recv(1024).decode()
    if passwordAttempt != password:
        #wrong password
        connectionSocket.close()
        return
    name = connectionSocket.recv(1024).decode()
    if name in nameSet or " " in name:
        #name already exists or name has space  
        connectionSocket.close()
    connectionSocket.send("Welcome!\n".encode())
    nameSet.add(name)
    joinAnnouncement = f"{name} joined the chatroom\n"
    #announce to all other clients that a new person has joined the chatroom
    serverPrint(joinAnnouncement)
    while True:
        msg = connectionSocket.recv(1024).decode()
        #handle exit
        if msg == ":Exit": 
            #connectionSocket.send(msg.encode())
            connectionSocket.close()
            clientDict.pop(addr)
            #remove name from set once client leaves
            nameSet.remove(name)
            #send message that user has left
            leaveMsg = f"{name} has left the chatroom\n"
            serverPrint(leaveMsg)
            for client in clientDict:
                clientDict[client].send(leaveMsg.encode())
            return
        outMsg = f"{name}: {msg}"
        #send message to all clients
        for client in clientDict:
            clientDict[client].send(outMsg.encode())
def main():
    args = sys.argv
    PORT = int(args[1])
    PASSWORD = args[2]
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', PORT))
    serverSocket.listen(1)
    serverPrint(f"Server started on port {PORT}. Accepting connections...\n")
    clientDict = dict() #dict of all clients. Key is client address, value is the socket object 
    threadDict = dict() #dict of all threads. Key is client address, value is the thread it is running on
    nameSet = set() #set of all names on the server
    while True:
        try:
            connectionSocket, addr = serverSocket.accept()
            clientDict[addr] = connectionSocket
            #start new thread
            threadDict[addr] = threading.Thread(target=clientThread, 
                                                args = (connectionSocket, addr, PASSWORD, nameSet, clientDict)) 
            #allows killing the thread
            threadDict[addr].daemon = True
            threadDict[addr].start()
        except KeyboardInterrupt:
            sys.exit()

if __name__ == "__main__":
    main()
