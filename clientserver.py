import socket
from threading import Thread

import sys
import time

HOST, PORT = '10.42.0.3', 8000#'2601:282:8001:4660::fe16', 80 # '192.168.137.3', 80 # '10.0.0.209', 80

class ClientServer(Thread):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):
        Thread.__init__(self)
    
    def sendMsg(self):
        while True:
            msg = 'test'

            self.sock.send(bytes(msg, 'utf-8'))
            time.sleep(1)
    
    def run(self):
        # connected = False

        # failcount = 0
        # while not connected:
            # try:
        info = socket.getaddrinfo(HOST, PORT)
        print(info)
        print(info[0][-1])

        self.sock.connect((HOST, PORT))

            #     connected = True
            # except Exception:
            #     failcount += 1
            #     print('Fail #' + str(failcount))
        
        msgThread = Thread(target=self.sendMsg())
        msgThread.start()

        while True:
            data = self.sock.recv(1024)
            if not data:
                print('Disconnected')
                break
            print(str(data, 'UTF-8'))

if __name__ == "__main__":
    server = ClientServer()
    server.start()

    input()