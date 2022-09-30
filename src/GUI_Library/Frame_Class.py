from PySide2.QtWidgets import QFrame


class FrameClass(QFrame):

    def __init__(self, parent=None, name="New_Frame", location_xy=(0, 0), size_wl=(20, 20),
                 style="",
                 shape=QFrame.StyledPanel, shadow=QFrame.Raised):
        super(FrameClass, self).__init__()
        self._set_parent(parent)
        self._set_style(style)
        self._set_name(name)
        self._set_location(location_xy[0], location_xy[1])
        self._set_size(size_wl[0], size_wl[1])
        self._set_shape(shape)
        self._set_shadow(shadow)

    def _set_name(self, name):
        self.setObjectName(name)

    def _set_parent(self, parent):
        self.setParent(parent)

    def _set_location(self, location_x, location_y):
        self.move(location_x, location_y)

    def _set_size(self, width, length):
        self.resize(width, length)

    def _set_style(self, style):
        self.setStyleSheet(style)

    def _set_shape(self, shape):
        self.setFrameShape(shape)

    def _set_shadow(self, shadow):
        self.setFrameShadow(shadow)

    def _set_visible(self, b_visible):
        self.setVisible(b_visible)

    def _set_enabled(self, b_enabled):
        self.setEnabled(b_enabled)

    def _set_fixed_width(self, width):
        self.setFixedWidth(width)

    def _set_maximum_height(self, height):
        self.setMaximumHeight(height)

    def _set_minimum_height(self, height):
        self.setMinimumHeight(height)

    def __del__(self):
        pass