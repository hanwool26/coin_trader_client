import logging
import socket
import threading
import json
import time

class Socket_Client():
    def __init__(self, config):
        self.config = config
        self.client_sock = None
        self.threads = [threading.Thread(target=self.__recv, daemon=False), ]

        self.conn_status = False
        self.ui_control = None
        self.config.load_config()

    def send(self, data):
        print('send+')
        if self.conn_status != True:
            logging.getLogger('LOG').info('서버와 미연결')
        else:
            self.client_sock.sendall(data.encode())

    def set_ui_control(self, ui_control):
        self.ui_control = ui_control

    def __recv(self):
        while self.conn_status and self.client_sock!=None:
            try:
                data = self.client_sock.recv(1024)
                if data != b'':
                    data = json.loads(data.decode())
                    command = data['command']
                    self.ui_control.signal_handler(command, data)
            except Exception as e:
                logging.getLogger('LOG').error(f'recv() : {e}')

    def disconnection(self):
        data = 'disconnect'
        self.client_sock.sendall(data.encode())
        self.conn_status = False
        time.sleep(2)
        self.client_sock.close()
        self.client_sock = None

    def connection_thread(self):
        print('connection_thread +')
        threads = [
            threading.Thread(target=self.__recv, daemon=False),
        ]
        for t in threads:
            t.start()

    def send_access_key(self):
        signal = {'command':'account'}
        signal.update({'access_key':self.config.access_key, 'secret_key':self.config.secret_key})
        signal = json.dumps(signal)
        try:
            self.send(signal)
        except Exception as e:
            print(e)

    def connection(self):
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_sock.connect((self.config.address, self.config.port))
            status = self.client_sock.recv(1024)
            print('status : ', status.decode())
            if status.decode() == 'connect':
                self.conn_status = True
                self.send_access_key()
                self.connection_thread()
            else:
                logging.getLogger('LOG').info("연결 실패")
        except Exception as e:
            logging.getLogger('LOG').error(e)
        # for t in self.threads:
        #    t.start()

