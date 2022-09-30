from PySide2.QtWidgets import QFrame, QLabel
from PySide2.QtCore import Qt


class BoxClass(QFrame):

    def __init__(self, parent=None, name="New_Frame", geometry=(), style="", b_show=None):
        super(BoxClass, self).__init__()
        self.set_parent(parent)
        self.set_style(style)
        self.set_name(name)
        self.set_geometry(geometry)
        self.set_visible(b_show)

        self.label = QLabel(self)
        self.label.setObjectName(name+"_label")
        self.label.setText(name)
        self.label.setFixedSize(self.width(), self.height())
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("QLabel {background-color: rgba(0,0,0,0);"
                                                             "color: rgba(0,0,0,255);}")
        self.label.setVisible(b_show)

    def set_name(self, name):
        self.setObjectName(name)

    def set_parent(self, parent):
        self.setParent(parent)

    def set_geometry(self, geometry):
        if geometry != ():
            x, y, w, h = geometry
            self.setGeometry(x, y, w, h)

    def set_style(self, style):
        self.setStyleSheet(style)

    def set_visible(self, b_visible):
        self.setVisible(b_visible)

    def __del__(self):
        pass


if __name__ == "__main__":
    # TEST CODE
    from PySide2.QtWidgets import QApplication
    from sys import exit

    # create Pyside2 app
    App = QApplication()

    # create the instance of our PyScreenUtility
    box = BoxClass(b_show=True, name="BOX")

    # start the app
    exit(App.exec_())
