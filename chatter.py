############################################################
# Author:       Aravind Potluri <aravindswami135@gmail.com>
# Description:  UDP based chat application, that send and
#               receives data on different threads.
############################################################

# Macros
# nodeIP = input("Enter Node's IP: ")
nodeIP = "172.23.203.197"
nodePort = 8080

# Libraries
import socket
import threading

# Install non standard modules
# requiredModules = ["keyboard"]
# for module in requiredModules:
#     try:
#         importlib.import_module(module)
#     except ImportError:
#         print(f"[!] {module} not found. Attempting to install...")
#         try:
#             subprocess.check_call(['pip', 'install', module])
#             print(f"[#] {module} has been successfully installed.")
#             importlib.import_module(module)
#         except Exception as e:
#             print(f"[!] Failed to install {module}. Error: {str(e)}")
#             exit()

# Functions to be run as processes
def receiveMsg(ip, port):
    """Used for receiving the messages"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", port))
    while True:
        try:
            data, nodeAddr = sock.recvfrom(1024)
            if ip == nodeAddr[0]:
                print(f"\n[{nodeIP}] : {data.decode('UTF-8')}")
            else:
                print("\n[!] Intrusion detected !!!")
        except KeyboardInterrupt:
            print("\n\n[!] Receiver Application terminated")
            break
    sock.close()

def sendMsg(ip, port):
    """Used for sending the messages"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True: 
        keyEvent = input()  
        try:
            if keyEvent == "":
                msg = input("[127.0.0.1] : ")
                sock.sendto(msg.encode('UTF-8'), (ip, port))
        except KeyboardInterrupt:
            print("\n\n[!] Sender Application terminated")
            break
    sock.close()

if __name__ == "__main__":
    print("############# pyChatter ################")
    # Create separate processes for sending and receiving messages
    rxProcess = threading.Thread(target=receiveMsg, args=(nodeIP,nodePort,))
    txProcess = threading.Thread(target=sendMsg, args=(nodeIP, nodePort,))
    try:
        # Start the receiving and sending processes
        rxProcess.start()
        txProcess.start()
        # Waiting for both processes to finish
        rxProcess.join()
        txProcess.join()
    except KeyboardInterrupt:
        print("\n\n[!] Application terminated")
        exit()
