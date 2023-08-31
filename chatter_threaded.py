############################################################
# Author:       Aravind Potluri <aravindswami135@gmail.com>
# Description:  UDP based chat application, that send and
#               receives data on different threads.
############################################################

# Macros
nodeIP = "172.17.50.136"
# nodeIP = input("Enter Node's IP: ")
nodePort = 8080

# Libraries
import socket
import threading
import sys

# Thread Functions
def sendMsg():
    """Parent Process: Used for sending the messages"""
    while True:
        try:
            msg = input("[127.0.0.1] : ")
            if msg == "quit":
                sock.close()
                exit()
            sock.sendto(msg.encode('UTF-8'), (nodeIP, nodePort))
        except KeyboardInterrupt:
            print("\n\n[!] Application terminated")
            break

def receiveMsg():
    """Child Process: Used for receiving the messages"""
    while True:
        data, nodeAddr = sock.recvfrom(1024)
        print(f"[{nodeIP}] : {data.decode('UTF-8')}")
        sys.stdin.read()

# The Main
if __name__ == "__main__":
    # Creating the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", nodePort))

    # Send and Receive functions are threaded
    txMsg = threading.Thread(target=sendMsg)
    rxMsg = threading.Thread(target=receiveMsg)
    txMsg.start()
    rxMsg.start()
    txMsg.join()
    rxMsg.join()

    # Termination
    sock.close()
    exit()

