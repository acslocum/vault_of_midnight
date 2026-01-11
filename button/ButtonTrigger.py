import configparser
from PyQt6.QtCore import (
    QObject,
    QTimer,
    pyqtSignal,
    pyqtSlot
)
import os

if os.path.exists('/etc/rpi-issue'):
    import RPi.GPIO as GPIO
    rpi = True
else:
    from blessed import Terminal
    rpi = False


class ButtonTrigger(QObject):
    triggered = pyqtSignal(str)
    
    def __init__(self, config : configparser.ConfigParser, parent = None):
        super().__init__(parent)
        self.config = config
        self.section = 'button_params'
        self.button = None
        if rpi:
            self.button = self.config.get(self.section, 'pin')
            print(f'ButtonTrigger: watching pin {self.button}')

        self.timeout = int(self.config.get(self.section, 'interval'))

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.slotTimeout)
        self.timer.start(self.timeout)

    @pyqtSlot()
    def slotTimeout(self):
        if rpi:
            # check assigned GPIO pin (and debounce)
            pass
        else:
            # watch keyboard for key press
            term = Terminal()            
            # Context manager to enter terminal's cbreak mode for immediate key detection
            with term.cbreak():
                key = term.inkey(timeout=self.timeout/2)

            if key:
                print(f"Key pressed: '{key.name if key.is_sequence else key}'")
                self.triggered.emit('')
                return key
            else:
                print("Timeout exceeded. No key pressed.")
                return None
