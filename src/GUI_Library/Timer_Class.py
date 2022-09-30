from PySide2.QtCore import QTimer, Qt


class TimerClass(QTimer):
    """
        parent: set object's parent
        timer_type: Select timer precision resolution 0 for best 2 for least
    """
    timer_type_list = [Qt.PreciseTimer, Qt.CoarseTimer, Qt.VeryCoarseTimer]

    def __init__(self, parent=None, timer_type=None):
        super(TimerClass, self).__init__(parent)
        self.set_timer_type(timer_type)

    ####################  SETTERS  ####################
    def set_timer_type(self, timer_type):
        if isinstance(timer_type, int):
            self.setTimerType(TimerClass.timer_type_list[timer_type])
        else:
            self.setTimerType(timer_type)

    def set_timeout_connect(self, slot):
        self.timeout.connect(slot)

    def stop_timer(self):
        if self.isActive():
            self.stop()

    def start_timer(self, interval_ms=0):
        if not self.isActive():
            self.start(interval_ms)
