# Python Libraries
from winsound import Beep


class NotificationManagerClass:

    def __init__(self):
        pass

    ####################  EMAIL NOTIFICATIONS  ####################

    ####################  AUDIO NOTIFICATIONS  ####################
    @staticmethod
    def alert_audio(freq: int = 400, msec: int = 1000):
        Beep(freq, msec)