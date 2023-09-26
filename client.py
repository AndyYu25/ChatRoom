import sys
from socket import *
import time
import datetime
import threading

def serverPrint(inStr: str):
    print(inStr, end = '', flush = False)

def serverThread(clientSocket: socket, closeEvent: threading.Event):
    """
    Function to monitor incoming server messages separately from monitoring stdin
    """
    #thread closes when the main thread closes
    while True:
        inMessage = clientSocket.recv(1024).decode()
        if inMessage == ":Exit":
            clientSocket.close()
            closeEvent.set()
            return
        serverPrint(inMessage)

def getDatetimeString():
    currentDatetime = datetime.datetime.now().replace(second = 0, microsecond=0)
    weekday = currentDatetime.strftime('%A')[:3]
    day = currentDatetime.day
    if day < 10:
        dayStr = "0" + str(day)
    else:
        dayStr = str(day)
    month = currentDatetime.month
    if month == 1:
        monthStr = "Jan"
    elif month == 2:
        monthStr = "Feb"
    elif month == 3:
        monthStr = "Mar"
    elif month == 4:
        monthStr = "Apr"
    elif month == 5:
        monthStr = "May"
    elif month == 6:
        monthStr = "Jun"
    elif month == 7:
        monthStr = "Jul"
    elif month == 8:
        monthStr = "Aug"
    elif month == 9:
        monthStr = "Sep"
    elif month == 10:
        monthStr = "Oct"
    elif month == 11:
        monthStr = "Nov"
    elif month == 12:
        monthStr = "Dec"
    year = currentDatetime.year
    hour = currentDatetime.hour
    if hour < 10:
        hourStr = "0" + str(hour)
    else:
        hourStr = str(hour)
    minute = currentDatetime.minute
    return f"It's {hourStr}:{minute} on {weekday}, {dayStr} {monthStr}, {year}\n"
def main():
    args = sys.argv
    HOST = args[1]
    PORT = int(args[2])
    password = args[3]
    name = args[4]
    serverPrint(f"Connecting to {HOST} on port {PORT}...\n")
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((HOST, PORT))
    clientSocket.send(f"{password}\n".encode())
    time.sleep(0.001)
    clientSocket.send(f"{name}\n".encode())
    welcomeMessage = clientSocket.recv(1024)
    serverPrint(welcomeMessage.decode())
    closeEvent = threading.Event()
    serverMonitor = threading.Thread(target=serverThread, 
                                            args = (clientSocket,closeEvent))
    serverMonitor.daemon = True
    serverMonitor.start()
    while True:
        cmdStr = input("")
        if cmdStr == ":Exit":
            clientSocket.send((cmdStr + "\n").encode())
            #wait for server response and for child thread to end
            time.sleep(1)
            closeEvent.set()
            clientSocket.close()
            sys.exit(0)
        elif cmdStr == ":)":
            clientSocket.send("[feeling happy]\n".encode())
        elif cmdStr == ":(":
            clientSocket.send("[feeling sad]\n".encode())
        elif cmdStr == ":mytime":
            clientSocket.send(getDatetimeString().encode())
        else:
            clientSocket.send((cmdStr + "\n").encode())

    

if __name__ == "__main__":
    main()
