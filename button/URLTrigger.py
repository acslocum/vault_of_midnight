import configparser
import urllib.request
from PyQt6.QtCore import (
    QObject,
    pyqtSignal
)


# WORK IN PROGRESS!!! NOT IMPLEMENTED YET
CONFIG_SERVER_URL = "server_url"

class URLTrigger(QObject):
    triggered = pyqtSignal(str)

    def __init__(self, config : configparser.ConfigParser, parent = None):
        super().__init__(parent)
        self.config = config


