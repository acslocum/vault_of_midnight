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
import signal

# import player classes
import AudioPlayer
import ConsolePlayer
import VideoPlayer

# import trigger classes
import ButtonTrigger
import TimerTrigger
import URLTrigger
import MQTTTrigger

kill_process = False
config = None

def read_configuration():
    config_ini = configparser.ConfigParser(allow_unnamed_section=True, inline_comment_prefixes=(';','#'))
    config_ini.read("config.ini")

    # debug specific parameters
    # print(f'debug: {config_ini.get('general', 'debug')}')
    # print(f'test: {config_ini.get('general', 'test')}')
    # print(f'player type: {config_ini.get('general', 'type')}')
    # print(f'trigger type: {config_ini.get('general', 'trigger_type')}')
    # print(f'random: {config_ini.get('general', 'random')}')
    # print(f'media_folder: {config_ini.get('general', 'media_folder')}')
    
    return config_ini

def signal_handler(sig, frame):
    """Handle the Ctrl+C signal for a graceful exit."""
    print("Caught Ctrl+C signal. Shutting down gracefully.")
    QApplication.quit()

if __name__ == "__main__":
    app = None
    player = None
    trigger = None
    signal.signal(signal.SIGINT, signal_handler)

    try:
        config = read_configuration()
        #print(config.options('general'))

        app = QApplication(sys.argv)
        # create the correct player based on type
        media_type = config.get('general', 'type')
        if media_type == 'audio':
            print('Creating audio player')
            player = AudioPlayer.AudioPlayer(config)
        elif media_type == 'console':
            print('Creating console player')            
            player = ConsolePlayer.ConsolePlayer(config)
        elif media_type == 'video':
            print('Creating video player')
            player = VideoPlayer.VideoPlayer(config)
            player.show()   
        else:
            print(f'Unknown type, \'{media_type}\' exiting...')
            exit()
        
        # create the correct type of trigger
        trigger_type = config.get('general', 'trigger_type')
        if trigger_type == 'timer':
            trigger = TimerTrigger.TimerTrigger(config)
        elif trigger_type == 'url':
            trigger = URLTrigger.URLTrigger(config)
        elif trigger_type == 'button':
            # if we're not on a Pi and media is video, we'll just tell Qt
            # to watch for keyboard events for test
            if ButtonTrigger.rpi == False:
                if media_type == 'video':
                    player.watchKeyEvents = True
            else:
                # we're on a Pi, just create a standard button trigger object
                trigger = ButtonTrigger.ButtonTrigger(config)
        elif trigger_type == 'mqtt':
            trigger = MQTTTrigger.MqttClient(config)
            trigger.connectToHost()
        else:
            print(f'Unknown trigger type: {trigger_type}')

        if player is not None:
            if trigger is not None:
                trigger.triggered.connect(player.triggered)
            sys.exit(app.exec())
        else:
            print('Error creating application event loop')
            exit(-1)
    except KeyboardInterrupt:
        # Perform any necessary cleanup here before exiting
        print("Ctrl+C pressed. Exiting gracefully.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(-1)