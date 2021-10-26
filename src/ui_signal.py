

class UI_Signal():
    def __init__(self, main_window):
        self.ui_control = main_window

    def signal_handler(self, command, data):
        if command == 'view_update':
            row = data['ev_id']
            info = data['info_list']
            self.ui_control.infinite_item_update(row, info)
        elif command == 'asset_update':
            pass

