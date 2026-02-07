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
                print(f'Setting RPi GPIO mode to BOARD')
                GPIO.setmode(GPIO.BOARD)
            elif self.config.get(self.section, 'gpio_mode') == 'BCM':
                print(f'Setting RPi GPIO mode to BCM')
                GPIO.setmode(GPIO.BCM)

            # Set up the pin as an input with a pull-up or pull-down resistor
            # This example uses a pull-up, so the button should connect to ground when pressed
            GPIO.setup(self.button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

            # Add event detection with a bouncetime of 200ms
            # The callback function will only be called once every 200ms
            GPIO.add_event_detect(self.button, GPIO.FALLING, callback=self.gpioCallback, bouncetime=self.debounce)
        else:
            raise Exception("ButtonTrigger only works on a Pi so far")

    def gpioCallback(self, channel):
        print(f"Button pressed on channel {channel}!")
        self.triggered.emit('')
