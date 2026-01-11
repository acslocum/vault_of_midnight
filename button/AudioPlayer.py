import configparser
import os
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QUrl
import pygame
import random
import time

class AudioPlayer(QObject):
    def __init__(self, config : configparser.ConfigParser):
        super().__init__()
        self.config = config
        self.files : list[str] = []
        self.media_dir_valid = False
        self.idle_valid = False

        pygame.mixer.init()
        self.media_dir = config.get('general', 'media_folder')
        self.idle = config.get('audio', 'idle_audio')
        if not os.path.isdir(self.media_dir):
            print(f'ERROR: AudioPlayer: media directory {self.media_dir} does not exist')
        else:
            self.media_dir_valid = True
        if not os.path.isfile(os.path.join(self.media_dir, self.idle)):
            print(f'ERROR: AudioPlayer: idle audio {self.idle} does not exist')
        else:
            self.idle_valid = True

            pygame.mixer.music.load(os.path.join(self.media_dir, self.idle))
            pygame.mixer.music.play(loops=-1)

        if self.media_dir_valid and self.idle_valid:
            self.load_files()

    def load_files(self):
        files = os.listdir(self.media_dir)
        files.remove(self.idle)
        self.files = files
        #print(self.files)

    @pyqtSlot(str)
    def triggered(self, filename : str):
        if len(filename) == 0:
            # choose random file to play from list
            filename = os.path.join('.', self.media_dir, random.choice(self.files)) 
            #print(f'Audio Player randomly playing: {filename}')
        else:
            #print(f'Audio Player playing requested: {filename}')
            pass

        # player should always be playing idle.mp3
        pygame.mixer.music.fadeout(300)

        try:
            print(f"Playing {filename}...")
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            # Keep the script running while the music plays
            while pygame.mixer.music.get_busy():
                time.sleep(1)
            pygame.mixer.music.load(os.path.join(self.media_dir, self.idle))
            pygame.mixer.music.play(loops=-1)
        except pygame.error as e:
            print(f"Error playing music: {e}")
        except KeyboardInterrupt:
            # Stop the music and quit on user interruption (e.g., Ctrl+C)
            pygame.mixer.music.stop()
            pygame.quit()
