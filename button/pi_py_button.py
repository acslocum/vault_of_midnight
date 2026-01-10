import sys
from PyQt6.QtWidgets import (
    QApplication
)
from PyQt6.QtCore import (
    QCoreApplication
)

from pathlib import Path
from time import sleep
import configparser

# import player classes
import AudioPlayer
import ConsolePlayer
import VideoPlayer

# import trigger classes
import TimerTrigger
#import URLTrigger
#import ButtonTrigger

kill_process = False
config = None

def read_configuration():
    config_ini = configparser.ConfigParser(allow_unnamed_section=True)
    config_ini.read("config.ini")
    return config_ini

if __name__ == "__main__":
    app = None
    player = None
    trigger = None

    config = read_configuration()
    #print(config.options('general'))

    # create the correct type of application based on media type
    media_type = config.get('general', 'type')
    if media_type == 'audio':
        print('Audio only, creating QCoreApplication')
        app = QCoreApplication(sys.argv)
        player = AudioPlayer.AudioPlayer(config)
    elif media_type == 'console':
        print('Audio only, creating QCoreApplication')
        app = QCoreApplication(sys.argv)
        player = ConsolePlayer.ConsolePlayer(config)
    elif media_type == 'video':
        print('Video, creating QApplication')
        app = QApplication(sys.argv)
        player = VideoPlayer()
        player.show()   
    else:
        print(f'Unknown type, \'{media_type}\' exiting...')
        exit()
    
    # create the correct type of trigger
    trigger_type = config.get('general', 'trigger_type')
    if trigger_type == 'timer':
        trigger = TimerTrigger.TimerTrigger(config)
    else:
        print(f'Unknown trigger type: {trigger_type}')

    if app is not None and player is not None and trigger is not None:
        trigger.triggered.connect(player.triggered)
        sys.exit(app.exec())
    else:
        print('Error creating application event loop')
        exit(-1)
