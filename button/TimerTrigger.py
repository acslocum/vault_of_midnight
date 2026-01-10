import configparser
from PyQt6.QtCore import (
    QObject,
    QTimer,
    pyqtSignal,
    pyqtSlot
)


class TimerTrigger(QObject):
    triggered = pyqtSignal(str)
    
    def __init__(self, config : configparser.ConfigParser, parent = None):
        super().__init__(parent)
        self.config = config
        self.timeout = int(self.config.get('timer_params', 'interval'))
        print(f'TimerTrigger: setting timeout to {self.timeout} ms')

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.slotTimeout)
        self.timer.start(self.timeout)

    @pyqtSlot()
    def slotTimeout(self):
        self.triggered.emit('')
