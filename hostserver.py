import socket
from threading import Thread

class HostServer(Thread):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []

    def __init__(self):
        self.sock.bind(('0.0.0.0', 8000))#('0.0.0.0', 8000))#
        self.sock.listen(5)
    
    def handler(self, c, a):
        while True:
            data = c.recv(1024)

            print(data)

            for connection in self.connections:
                connection.send(data)
                if not data:
                    break;
    
    def run(self):
        while True:
            c,a = self.sock.accept()

            cThread = Thread(target=self.handler, args=[c, a])
            cThread.start()

            self.connections.append(c)
            print(c)

if __name__ == "__main__":
    host = HostServer()
    host.run()

    input()