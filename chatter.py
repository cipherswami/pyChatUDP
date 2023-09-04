############################################################
# Author:       Aravind Potluri <aravindswami135@gmail.com>
# Description:  UDP based chat application, that send and
#               receives data on different threads.
############################################################

# Macros
nodeIP = input("Enter Node's IP: ")
nodePort = int(input("Enter Port: "))
doRun = True

# Libraries
import socket
import threading
import signal

# Functions to be run as threads
def receiveMsg(sock, ip, port):
    """Used for receiving the messages"""
    sock.bind(("0.0.0.0", port))
    while doRun:
        try:
            data, nodeAddr = sock.recvfrom(1024)
            if ip == nodeAddr[0]:
                """To check if it is from the right source"""
                print(f"\n[{nodeIP}] : {data.decode('UTF-8')}")
            elif "127.0.0.1" == nodeAddr[0]:
                """This is the termination signal"""
                break
            else:
                """Intrusion check"""
                print(f"\n[!] Intrusion detected: {nodeAddr}")
        except KeyboardInterrupt:
            break
    sock.close()
    exit()

def sendMsg(sock, ip, port):
    """Used for sending the messages"""
    while doRun:  
        try:
            keyEvent = input() 
            if keyEvent == "":
                try:
                    msg = input("[127.0.0.1] : ")
                    sock.sendto(msg.encode('UTF-8'), (ip, port))
                except KeyboardInterrupt:
                    break
        except KeyboardInterrupt:
            break
        except EOFError:
            break
    sock.sendto(msg.encode('UTF-8'), ('127.0.0.1', port)) # Termination signal
    sock.close()
    exit()

def handle_sigint(signum, frame):
    """Function to handle SIGINT"""
    global doRun
    doRun = False

if __name__ == "__main__":
    print("############# pyChatter ################")

    # Creating Sockets
    rxSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    txSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Create separate processes for sending and receiving messages
    rxProcess = threading.Thread(target=receiveMsg, args=(rxSock, nodeIP,nodePort,))
    txProcess = threading.Thread(target=sendMsg, args=(txSock, nodeIP, nodePort,))

    # Start the receiving and sending processes
    txProcess.start()
    rxProcess.start()

    signal.signal(signal.SIGINT, handle_sigint)
    
    # Waiting for processes to join
    rxProcess.join()
    txProcess.join()

    print("\n[!] Application terminated")
    exit()