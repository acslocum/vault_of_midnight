import configparser
import urllib.request
from PyQt6.QtCore import (
    QObject,
    QTimer,
    pyqtSignal,
    pyqtSlot
)
import os

class URLTrigger(QObject):
    triggered = pyqtSignal(str)

    def __init__(self, config : configparser.ConfigParser, parent = None):
        super().__init__(parent)
        self.config = config
        self.media_dir = config.get('general', 'media_folder')
        self.config_section = 'url_params'
        self.poll_interval = int(self.config.get(self.config_section, 'interval'))
        self.poll_timeout = int(self.config.get(self.config_section, 'timeout')) / 1000 # request wants timeout in seconds
        self.url = self.config.get(self.config_section, 'server_url')
        self.random_keyword = self.config.get(self.config_section, 'random_keyword')
        
        print(f'URLTigger: endpoint is {self.url}')
        print(f'URLTrigger: setting interval to {self.poll_interval} ms, timeout to {self.poll_timeout} s')

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.slotPoll)
        self.timer.start(self.poll_interval)

    @pyqtSlot()
    def slotPoll(self):
        try:
            contents = urllib.request.urlopen(url=self.url, 
                                              timeout=self.poll_timeout).read()
            if contents:
                utf8 = contents.decode('utf-8')
                print(f'Received: \'{utf8}\'')
                if utf8 == self.random_keyword:
                    self.triggered.emit('')
                else:
                    filename = os.path.join('.', self.media_dir, utf8)
                    self.triggered.emit(filename)
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
