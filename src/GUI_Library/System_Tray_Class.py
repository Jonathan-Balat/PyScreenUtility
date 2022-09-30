from PySide2.QtWidgets import QSystemTrayIcon


class SystemTrayIcon(QSystemTrayIcon):

    __activation_reasons_dict = {
        "double_click": QSystemTrayIcon.DoubleClick,
        "middle_click": QSystemTrayIcon.MiddleClick,
        # SystemTrayIcon.Trigger:  # Left click
        # SystemTrayIcon.Unknown:
        # SystemTrayIcon.Context:  # Right click
    }

    def __init__(self, parent=None, name="New_Tray_Widget", icon=None):
        super(SystemTrayIcon, self).__init__()

        self.__tray_state_dict = {}
        self.__assigned_reasons_dict = {}

        self.set_parent(parent)
        self.set_name(name)
        self.set_icon(icon)

        self.activated.connect(self.__tray_activation_event)

    ####################  SETTERS  ####################
    def set_parent(self, parent):
        self.setParent(parent)

    def set_name(self, name):
        self.setObjectName(name)

    def set_location(self, location_x, location_y):
        self.move(location_x, location_y)

    def set_size(self, width, length):
        self.resize(width, length)

    def set_style(self, style):
        self.setStyleSheet(style)

    def set_visible(self, b_visible):
        self.setVisible(b_visible)

    def set_enabled(self, b_enabled):
        self.setEnabled(b_enabled)

    def set_fixed_width(self, width):
        self.setFixedWidth(width)

    def set_maximum_height(self, height):
        self.setMaximumHeight(height)

    def set_minimum_height(self, height):
        self.setMinimumHeight(height)
        
    def set_icon(self, icon):
        self.setIcon(icon)

    def set_tool_tip(self, tool_tip_message: str):
        self.setToolTip(tool_tip_message)

    def set_notification_message(self, notification_tup: tuple):
        if None not in notification_tup:
            title, message, icon, time_ms = notification_tup
            self.showMessage(title, message, icon, time_ms)

    ####################  TRAY STATE MANAGEMENT  ####################
    def __state_check(self, state: str):
        b_valid = state in self.__tray_state_dict

        if not b_valid:
            print("State non-existent")

        return b_valid

    def add_tray_state(self, state_name: str, b_visible: bool, tool_tip_message: str, notification_message: tuple):
        self.__tray_state_dict[state_name] = (b_visible, tool_tip_message, notification_message)

    def remove_tray_state(self, state_name: str):
        if self.__state_check(state_name):
            _ = self.__tray_state_dict.pop(state_name)

    def change_tray_state(self, state_name):
        if self.__state_check(state_name):
            b_visible, tool_tip_message, notification_message = self.__tray_state_dict.get(state_name)

            self.set_visible(b_visible)
            self.set_tool_tip(tool_tip_message)
            self.set_notification_message(notification_message)

    ####################  ACTIVATION MANAGEMENT  ####################
    def set_activation_reason_slots(self, reason, function):
        reason = SystemTrayIcon.__activation_reasons_dict.get(reason)
        if reason is not None:
            self.__assigned_reasons_dict[reason] = function

    def __tray_activation_event(self, reason):
        print("Tray activation reason", reason)
        function = self.__assigned_reasons_dict.get(reason)
        if function is not None:
            function()

    def __del__(self):
        pass