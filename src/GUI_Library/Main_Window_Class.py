from PySide2.QtWidgets import QMainWindow


class MainWindowClass(QMainWindow):

    def __init__(self, name="New_MainWindow", size_wl=(500, 500), window_title="New_Window", min_height=20, min_width=20):
        super(MainWindowClass, self).__init__()
        self.set_name(name)
        self.set_size(size_wl[0], size_wl[1])
        self.set_window_title(window_title)
        self.set_min_height(min_height)
        self.set_min_width(min_width)

    ####################  SETTERS  ####################
    def set_name(self, name):
        self.setObjectName(name)

    # Sizing and location
    def set_min_height(self, min_height):
        self.setMinimumHeight(min_height)

    def set_min_width(self, min_width):
        self.setMinimumWidth(min_width)

    def set_size(self, width, length):
        self.resize(width, length)

    def set_fixed_size(self, width, height):
        self.setFixedSize(width, height)

    def set_geometry(self, x_pos, y_pos, width, height):
        self.setGeometry(x_pos, y_pos, width, height)

    def set_location(self, location_x, location_y):
        self.move(location_x, location_y)

    # Methods
    def set_style(self, style):
        self.setStyleSheet(style)

    def set_window_title(self, title):
        self.setWindowTitle(title)

    def set_central_widget(self, central_widget):
        self.setCentralWidget(central_widget)

    def set_status_bar(self, status_bar):
        self.setStatusBar(status_bar)

    def set_window_icon(self, icon):
        self.setWindowIcon(icon)

    def set_cursor(self, cursor):
        self.setCursor(cursor)

    def set_window_opacity(self, value: float):
        self.setWindowOpacity(value)

    def set_window_flag(self, flag_config):
        self.setWindowFlag(flag_config)

    def set_focus_policy(self, policy):
        self.setFocusPolicy(policy)

    def set_visible(self, b_flag: bool):
        self.setVisible(b_flag)

    ####################  GETTERS  ####################
    def _get_width(self):
        return self.width()

    def _get_height(self):
        return self.height()

    def __del__(self):
        pass