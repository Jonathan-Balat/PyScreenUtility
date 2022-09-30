from PySide2.QtGui import QIcon


class IconClass(QIcon):

    def __init__(self, icon_path=""):
        super(IconClass, self).__init__(icon_path)
