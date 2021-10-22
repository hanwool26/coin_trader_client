import socket
import threading
import json

class Socket_Client():
    def __init__(self, address, port):
        self.server_addr = address
        self.port = port

        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.threads = [threading.Thread(target=self.__recv, daemon=False), ]


    def __recv(self):
        while True:
            data = self.client_sock.recv(1024)
            if data != b'':
                print(data.decode())

    def connection(self):
        self.client_sock.connect((self.server_addr, self.port))
        for t in self.threads:
            t.start()


if __name__ == '__main__':
    client_sock = Socket_Client('10.157.8.216', 9999)
    client_sock.connection()
    TEST_JSON = {'coin_name': '리플',
                 'balance': 100000,
                 'interval': 6,
                 'repeat': False}
    data = json.dumps(TEST_JSON)

    client_sock.client_sock.sendall(data.encode())
