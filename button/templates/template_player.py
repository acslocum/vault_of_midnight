import configparser
from PyQt6.QtCore import QObject, Qt, pyqtSlot

class template_player(QObject):
    def __init__(self, config : configparser.ConfigParser, parent : QObject = None):
        super().__init__(parent)
        self.config = config
        self.config_section = 'section' # change to whatever section you want to use for this trigger

        # repeat a modified version of this call to pull out whatever parameters you need
        self.value = int(self.config.get(self.config_section, 'key'))
        
    @pyqtSlot(str)
    def triggered(self, filename : str):
        # do whatever you're supposed to do with 'filename'

        # NOTE: make sure you handle an empty string, '', 
        # as it is commonly used to indicate we want to
        # select a media file at random and play it
        pass