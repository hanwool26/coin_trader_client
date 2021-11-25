import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from src.util import UI_PATH, util_strip, get_price_by_name, get_RSI
from src import log

import os
import logging
import json

COUPLE_HEADER = ('선두코인', '후발코인', '결속력', '가격대', '비고', '진행상태', )
INFINITE_HEADER = ('코인', '현재가', '평단가', '평가금액', '평가손익', '수익률', '진행상태')
INFINITE_INTERVAL = [1,3,6,9,12,24]
ASSET_RATES = [10, 25, 50, 75, 100]

class MainWindow(QMainWindow):
    def __init__(self, socket, ui):
        super(MainWindow, self).__init__()

        if getattr(sys, 'frozen', False):
            res_path = os.path.realpath(sys.executable)
        elif __file__:
            res_path = os.path.realpath(__file__)
        # uic.loadUi(os.path.join(UI_PATH, 'main.ui'))
        ui.setupUi(self)
        icon_path = os.path.join(UI_PATH, 'Bitcoin_Cash.png')
        self.setWindowIcon(QIcon(icon_path))

        # self.couple_list = couple_list
        self.manager_handler = None
        self.socket = socket
        self.sel_id = list()
        self.trade = 'infinite'
        self.asset = 0
        self.invest_asset = 0

        self.list_view = self.findChild(QTableWidget, 'list_view')
        self.list_view.cellClicked.connect(self.cellclicked_event)
        self.max_row_count = 0

        self.trade_btn = self.findChild(QPushButton, 'trade_btn')
        self.trade_btn.clicked.connect(self.trade_btn_event)

        self.stop_btn = self.findChild(QPushButton, 'stop_btn')
        self.stop_btn.clicked.connect(self.stop_btn_event)

        self.connect_btn = self.findChild(QPushButton, 'connectButton')
        self.connect_btn.clicked.connect(self.connect_btn_event)

        self.disconnect_btn = self.findChild(QPushButton, 'disconnectButton')
        self.disconnect_btn.clicked.connect(self.disconnect_btn_event)
        self.disconnect_btn.setDisabled(True)

        self.asset_info = self.findChild(QLineEdit, 'asset_info')
        self.profit_info = self.findChild(QLineEdit, 'profit_lineEdit')

        self.invest_asset_lineedit = self.findChild(QLineEdit, 'invest_asset_lineEdit')

        # group box
        self.infinite_r_btn = self.findChild(QRadioButton, 'infinite_r_btn')
        self.infinite_r_btn.clicked.connect(self.radio_btn_event)

        # coin list combo box
        self.coin_combobox = self.findChild(QComboBox, 'coin_comboBox')
        self.coin_combobox.currentIndexChanged.connect(self.handle_coin_combobox)
        self.interval_combobox = self.findChild(QComboBox, 'interval_comboBox')
        self.asset_rate_combobox = self.findChild(QComboBox, 'asset_rate_comboBox')
        self.asset_rate_combobox.currentIndexChanged.connect(self.handle_asset_rate_combobox)

        self.update_asset_btn = self.findChild(QPushButton, 'asset_update_btn')
        self.update_asset_btn.clicked.connect(self.request_asset_info)

        self.auto_checkbox = self.findChild(QCheckBox, 'auto_checkBox')
        self.autonum_combobox = self.findChild(QComboBox, 'autonum_comboBox')


        self.log_view = self.findChild(QTextBrowser, 'log_view')
        self.log_handler = log.QTextEditLogger(self.log_view)
        self.log_handler.setFormatter(logging.Formatter('[%(asctime)s] %(message)s'))
        logging.getLogger('LOG').addHandler(self.log_handler)
        logging.getLogger('LOG').setLevel(logging.DEBUG)

    def update_info(self, info):
        self.profit_info.setText(info)

    def set_coule_table(self, couple_list):
        self.list_view.clear()
        header = COUPLE_HEADER
        self.list_view.setColumnCount(len(header))
        self.list_view.setHorizontalHeaderLabels(header)
        num_of_list = len(couple_list)
        self.list_view.setRowCount(num_of_list)

        for rownum, row in enumerate(couple_list):
            for col, val in enumerate(row):
                self.couple_item_update(rownum, col, val)

    def set_infinite_table(self):
        self.list_view.clear()
        header = INFINITE_HEADER
        self.list_view.setColumnCount(len(header))
        self.list_view.setHorizontalHeaderLabels(header)
        self.list_view.setRowCount(self.max_row_count)

    def set_asset_rate_combobox(self):
        for rate in ASSET_RATES:
            self.asset_rate_combobox.addItem(f'{str(rate)} %')
        self.asset_rate_combobox.setCurrentText('자산 비율')

    def handle_coin_combobox(self):
        current_coin = self.coin_combobox.currentText()
        current_price = get_price_by_name(current_coin)
        self.profit_info.setText(f'현재가 : {current_price}원 RSI : {get_RSI(current_coin)}')

    def handle_asset_rate_combobox(self):
        invest_str = self.asset * (int(util_strip(self.asset_rate_combobox.currentText())) / 100)
        self.invest_asset_lineedit.setText(f'{(round(invest_str, 2))} 원')

    def set_coin_combobox(self, coin_list):
        if coin_list == None:
            return
        for coin in coin_list:
            self.coin_combobox.addItem(coin)

    def set_interval_combobox(self):
        for time in INFINITE_INTERVAL:
            self.interval_combobox.addItem(f'{time} 시간')
        self.interval_combobox.setCurrentText('Interval')

    def set_autonum_combobox(self):
        for num in range(1, 10):
            self.autonum_combobox.addItem(str(num))
        self.autonum_combobox.setCurrentText('자동 코인 수')

    def set_max_row(self, row):
        self.max_row_count = row
        self.list_view.setRowCount(self.max_row_count)

    def infinite_item_update(self, row, val: list):
        print(val)
        if row >= self.max_row_count:
            self.max_row_count = row
        self.list_view.setRowCount(self.max_row_count+1)
        for idx, attr in enumerate(val):
            item = QTableWidgetItem(str(attr))
            if item !=None:
                self.list_view.setItem(row, idx, item)

    def couple_item_update(self, row, col, val):
        item = QTableWidgetItem(val)
        if item != None:
            self.list_view.setItem(row,col,item)

    def cellclicked_event(self, row, col):
        selected = self.list_view.selectedIndexes()
        self.sel_id = [idx.row() for idx in selected]

    def get_interval(self):
        try:
            hour = self.interval_combobox.currentText()
            return int(util_strip(hour))
        except Exception as e:
            logging.getLogger('LOG').error(f'Interval을 선택해주세요.')
            return 0

    def trade_btn_event(self):
        if self.auto_checkbox.isChecked():
            signal = {'command':'auto_trade_start',
                      'trade_num': int(self.autonum_combobox.currentText())}
        else :
            signal = {'command':'do_start'}
            self.invest_asset = (util_strip(self.invest_asset_lineedit.text()))
            signal.update({'trade':self.trade, 'coin_name':self.coin_combobox.currentText(), 'balance':self.invest_asset,
                           'interval':self.get_interval()})
        print(signal)
        signal = json.dumps(signal)
        self.socket.send(signal)

    def stop_btn_event(self):
        if self.auto_checkbox.isChecked():
            signal = {'command':'auto_trade_stop'}
        else:
            signal = {'command':'do_stop'}
            signal.update({'trade':self.trade, 'sel_id':self.sel_id})

        print(signal)
        signal = json.dumps(signal)
        self.socket.send(signal)

    def radio_btn_event(self):
        if self.infinite_r_btn.isChecked():
            self.trade = 'infinite'
            self.set_infinite_table()

    def connect_btn_event(self):
        if self.socket.conn_status == False:
            if self.socket.connection():
                self.connect_btn.setDisabled(True)
                self.disconnect_btn.setEnabled(True)
        else:
            logging.getLogger('LOG').info('연결중')

    def disconnect_btn_event(self):
        if self.socket.conn_status == True:
            self.socket.disconnection()
            self.connect_btn.setEnabled(True)
            self.disconnect_btn.setDisabled(True)
        else:
            logging.getLogger('LOG').info('연결 해제중')

    def set_manager_handler(self, manager):
        self.manager_handler = manager
        self.show_asset_info()

    def request_asset_info(self):
        signal = {'command':'request_asset'}
        signal = json.dumps(signal)
        self.socket.send(signal)

    def show_asset_info(self, asset):
        self.asset = asset
        asset_str = f'자산 : {self.asset} 원'
        self.asset_info.setText(asset_str)
        self.handle_coin_combobox()
