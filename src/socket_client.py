import socket

class Socket_Client():
    def __init__(self, address, port):
        self.server_addr = address
        self.port = port

        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connection(self):
        self.client_sock.connect((self.server_addr, self.port))

if __name__ == '__main__':
    

