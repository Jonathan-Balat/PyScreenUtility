from PySide2.QtWidgets import QMenu


class MenuClass(QMenu):

    def __init__(self, parent=None, title="Menu_Class"):
        super(MenuClass, self).__init__(parent=parent, title=title)

    def set_new_action(self, label: str, action):
        # TODO: Add more parameter control for addAction from this method
        self.addAction(label, action)

    def set_new_separator(self):
        self.addSeparator()
