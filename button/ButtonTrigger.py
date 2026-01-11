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
        self.debounce = int(self.config.get(self.section, 'debounce'))
        if rpi:
            self.button = int(self.config.get(self.section, 'pin'))
            print(f'ButtonTrigger: watching pin {self.button}')
            if self.config.get(self.section, 'gpio_mode') == 'BOARD':
                GPIO.setmode(GPIO.BOARD)
            elif self.config.get(self.section, 'gpio_mode') == 'BCM':
                GPIO.setmode(GPIO.BCM)

            # Set up the pin as an input with a pull-up or pull-down resistor
            # This example uses a pull-up, so the button should connect to ground when pressed
            GPIO.setup(self.button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

            # Add event detection with a bouncetime of 200ms
            # The callback function will only be called once every 200ms
            GPIO.add_event_detect(self.button, GPIO.FALLING, callback=self.gpioCallback, bouncetime=self.debounce)
        else:
            self.timeout = int(self.config.get(self.section, 'interval'))

            self.timer = QTimer(self)
            self.timer.timeout.connect(self.slotTimeout)
            self.timer.start(self.timeout)


    def gpioCallback(self, channel):
        print(f"Button pressed on channel {channel}!")
        self.triggered.emit('')

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
