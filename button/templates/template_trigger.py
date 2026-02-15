import configparser
from PyQt6.QtCore import (
    QObject,
    pyqtSignal,
    pyqtSlot
)

class trigger_template(QObject):
    triggered = pyqtSignal(str)
    
    def __init__(self, config : configparser.ConfigParser, parent : QObject = None):
        super().__init__(parent)
        self.config = config
        self.config_section = 'section' # change to whatever section you want to use for this trigger

        # repeat a modified version of this call to pull out whatever parameters you need
        self.value = int(self.config.get(self.config_section, 'key'))

    # call this function periodically to see if a guest did the thing
    @pyqtSlot()
    def checkForAction(self):
        actionOccurred = False

        # do whatever is needed to check if the action occurred

        # emit the signal if so
        if actionOccurred == True:
            self.triggered.emit('')
