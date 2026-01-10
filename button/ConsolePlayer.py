import configparser
from PyQt6.QtCore import QObject, Qt, pyqtSlot

class ConsolePlayer(QObject):
    def __init__(self, config : configparser.ConfigParser):
        super().__init__()
        self.config = config
        print('Console Player: Idle')
        
    @pyqtSlot(str)
    def triggered(self, filename : str):
        print(f'Console Player received: {filename}')
        print('Console Player: Idle')