from src.config import *
from main_window import *
from src.socket_client import *
from src.ui_signal import *
from ui.main_ui import *
import sys
from PyQt5.QtWidgets import *
from src.util import *
import qdarkstyle

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # files = LoadFile('couple_coin_list.xlsx')
    # couple_list = files.get_couple_list()
    config = Config()
    socket = Socket_Client(config)

    ui = Ui_MainWindow()
    mywindow = MainWindow(socket,ui)
    mywindow.setWindowTitle('DreamCoin')
    mywindow.set_infinite_table()

    ui_signal = UI_Signal(mywindow)

    # load UI items from file and set the list on listView
    # mywindow.set_table_data(couple_list)

    socket.set_ui_control(ui_signal)
    mywindow.set_coin_combobox(get_coin_list())
    mywindow.set_interval_combobox()
    mywindow.set_autonum_combobox()

    mywindow.set_asset_rate_combobox()
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    mywindow.show()
    app.exec_()
