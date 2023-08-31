############################################################
# Author:       Aravind Potluri <aravindswami135@gmail.com>
# Description:  UDP based chat application, that send and
#               receives data on different threads.
############################################################

# Macros
nodeIP = input("Enter Node's IP: ")
nodePort = 8080

# Libraries
import socket
import os

# Main function
def main():
    childPid = os.fork()
    if childPid == 0:
        """Parent Process: Used for sending the messages"""
        while True:
            try:
                msg = input("[127.0.0.1] : ")
                sock.sendto(msg.encode('UTF-8'), (nodeIP, nodePort))
            except KeyboardInterrupt:
                print("\n\n[!] Application terminated")
                break
    else:
        """Child Process: Used for receiving the messages"""
        while True:
            try:
                data, nodeAddr = sock.recvfrom(1024)
                print(f"[{nodeIP}] : {data.decode('UTF-8')}")
            except KeyboardInterrupt:
                break


# The Main
if __name__ == "__main__":
    
    # Creating the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", nodePort))

    # Start main
    main()

    # Termination
    sock.close()
    exit()

