import configparser
import os
import sys
from PyQt6.QtWidgets import (
    QMainWindow,
    QFrame,
    QVBoxLayout
)
from PyQt6.QtCore import QTimer, Qt, pyqtSlot
import random
from time import sleep
import vlc

idle_is_playing = True
CONFIG_VIDEO_PATH = "video_folder"
CONFIG_IDLE_VIDEO_NAME = "idle_video"

class VideoPlayer(QMainWindow):
    def __init__(self, config : configparser.ConfigParser, parent = None):
        super().__init__(parent=parent)
        self.config = config
        self.section = 'video'
        self.media_dir = config.get('general', 'media_folder')
        self.idle = config.get(self.section, 'idle_video')
        self.media_dir_valid = False
        self.idle_valid = False
        self.files = []
        self.fps_max = config.get(self.section, 'fps_max')
        self.requested_video_name = None
        if not os.path.isdir(self.media_dir):
            print(f'ERROR: VideoPlayer: media directory {self.media_dir} does not exist')
        else:
            self.media_dir_valid = True
        if not os.path.isfile(os.path.join(self.media_dir, self.idle)):
            print(f'ERROR: VideoPlayer: idle video {self.idle} does not exist')
        else:
            self.idle_valid = True
        if self.media_dir_valid and self.idle_valid:
            self.load_files()

        self.showFullScreen()

        # Create a VLC instance and a media player.
        self.instance = vlc.Instance()
        self.mediaplayer = self.instance.media_player_new()

        # Set up the main widget and layout.
        self.widget = QFrame(self)
        self.setCentralWidget(self.widget)
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)
        #self.widget.setWindowFlags(0x00000800)
        self.setStyleSheet("background-color: black;")

        # Create the video frame where VLC will render the video.
        self.video_frame = QFrame()
        self.video_frame.setStyleSheet("background: black; border: 0px; padding: 0px; margin: 0px")
        self.layout.addWidget(self.video_frame)

        self.setCursor(Qt.CursorShape.BlankCursor)

        #timer to check events
        self.timer = QTimer(self)
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.updateUI)
        self.timer.start()

    @pyqtSlot(str)
    def triggered(self, filename : str):
        if len(filename) > 0:
            print(f'Video Player selecting: {filename}')
        else:
            filename = random.choice(self.files)
        filename = os.path.join('.', self.media_dir, filename)
        self.requested_video_name = filename
    
    def load_files(self):
        files = os.listdir(self.media_dir)
        files.remove(self.idle)
        self.files = files
        #print(self.files)

    def video_directory(self):
        global CONFIG_VIDEO_PATH
        return f"{self.config[configparser.UNNAMED_SECTION][CONFIG_VIDEO_PATH]}"

    def play_idle_video(self):
        global idle_is_playing
        if(self.mediaplayer.is_playing()):
            return
        idle_is_playing = True
        self.open_file(os.path.join('.', self.media_dir, self.idle))
        return
    
    def updateUI(self):
        self.play_idle_video()
        if self.requested_video_name:
            print(f'updateUI: {self.requested_video_name}')
            self.play_video(self.requested_video_name)
            self.requested_video_name = None
            return

    def play_video(self, video):
        global idle_is_playing
        if (self.requested_video_name is not None) & (idle_is_playing == True):
            self.mediaplayer.stop()
            idle_is_playing = False
            self.open_file(video)
            self.timer.stop()
            sleep(2)
            self.timer.start()


    def open_file(self, video):
        # Open a file dialog to select a video file.
        self.filename = video
        if self.filename:
            media = self.instance.media_new(os.path.abspath(self.filename))
            self.mediaplayer.set_media(media)
            print(self.video_frame.winId())
            # Embed the VLC video output into our video frame.
            if sys.platform.startswith('linux'):
                self.mediaplayer.set_xwindow(int(self.video_frame.winId()))
            elif sys.platform == "win32":
                self.mediaplayer.set_hwnd(self.video_frame.winId())
            elif sys.platform == "darwin":
                self.mediaplayer.set_nsobject(int(self.video_frame.winId()))
            self.mediaplayer.play()
