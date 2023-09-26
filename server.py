from socket import *
import threading
import sys

def serverPrint(inStr: str, lock: threading.Lock):
    lock.acquire()
    print(inStr, end = '', flush = True)
    lock.release()

def clientThread(connectionSocket: socket, addr: str,
                 password: str, nameSet: dict, clientDict: dict,
                 printLock: threading.Lock):
    """
    operations for a single client
    """
    #check passcode
    #both messages come in as a single message to recv since
    #they are sent back-to-back
    login = connectionSocket.recv(1024).decode().split("\n")
    if login[0].strip() != password:
        #wrong password
        connectionSocket.close()
        return
    name = login[1]
    if name in nameSet.keys() or " " in name:
        #name already exists or name has space  
        connectionSocket.close()
        return
    connectionSocket.send("Welcome!\n".encode())
    nameSet[name] = addr
    joinAnnouncement = f"{name} joined the chatroom\n"
    #announce to all other clients that a new person has joined the chatroom
    serverPrint(joinAnnouncement, printLock)
    for client in clientDict:
        if client != addr:
            clientDict[client].send(joinAnnouncement.encode())
    while True:
        try:
            msg = connectionSocket.recv(1024).decode()
            if msg.strip()[:3] == ":dm" and len(msg.split(" ")) >= 3:
                #if a DM is recieved
                dm = msg.split(" ")
                destName = dm[1]
                directMsg = " ".join(dm[2:])
                destAddr = nameSet[destName]
                formattedDM = f"{name} -> {destName}: {directMsg}"
                serverPrint(formattedDM, printLock)
                clientDict[destAddr].send(formattedDM.encode())
                clientDict[addr].send(formattedDM.encode())
            elif msg != '':
                outMsg = f"{name}: {msg}"
                serverPrint(outMsg, printLock)
                #send message to all clients (including sender)
                for client in clientDict:
                    clientDict[client].send(outMsg.encode())
            else:
                raise Exception()
        except:
            #handle exit
            connectionSocket.close()
            clientDict.pop(addr)
            #remove name from set once client leaves
            nameSet.pop(name)
            #send message that user has left
            leaveMsg = f"{name} left the chatroom\n"
            serverPrint(leaveMsg, printLock)
            for client in clientDict:
                clientDict[client].send(leaveMsg.encode())
            return
            
def main():
    args = sys.argv
    PORT = int(args[1])
    PASSWORD = args[2]
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', PORT))
    serverSocket.listen(100)
    printLock = threading.Lock()
    serverPrint(f"Server started on port {PORT}. Accepting connections...\n", printLock)
    clientDict = dict() #dict of all clients. Key is client address, value is the socket object 
    threadDict = dict() #dict of all threads. Key is client address, value is the thread it is running on
    nameDict = dict() #dict of all names and their corresponding address

    while True:
        connectionSocket, addr = serverSocket.accept()
        clientDict[addr] = connectionSocket
        #start new thread
        threadDict[addr] = threading.Thread(target=clientThread, 
                                            args = (connectionSocket, addr, PASSWORD,
                                                    nameDict, clientDict, printLock)) 
        #allows killing the thread
        threadDict[addr].daemon = True
        threadDict[addr].start()
        

if __name__ == "__main__":
    main()
