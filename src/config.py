import configparser
import logging
import os
from src.util import DATA_PATH

class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.secret_key = ""
        self.access_key = ""
        self.address = ""
        self.port = 0
        self.CONFIG_PATH = os.path.join(DATA_PATH, '../data/config.ini')


    def load_config(self):
        self.config.read(self.CONFIG_PATH, encoding='utf-8')
        self.access_key = self.config['api_key']['access_key']
        self.secret_key = self.config['api_key']['secret_key']
        self.address = self.config['socket']['address']
        self.port = self.config['socket']['port']


    def get_api_key(self):
        if len(self.access_key)!=0 and len(self.secret_key)!=0:
            return self.access_key, self.secret_key
        else:
            logging.info("No data in api key")

    def get_socket_info(self):
        if len(self.address)!=0 and len(self.port)!=0:
            print(self.address, self.port)
            return self.address, int(self.port)
        else:
            logging.info("No data in socket")
