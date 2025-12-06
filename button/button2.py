import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFrame,
    QVBoxLayout
)
from PyQt6.QtCore import QTimer, Qt
import vlc
from pathlib import Path

import configparser
import urllib.request

kill_process = False
requested_video_name = None
idle_is_playing = True
CONFIG_VIDEO_PATH = "video_folder"
CONFIG_IDLE_VIDEO_NAME = "idle_video"
CONFIG_SERVER_URL = "server_url"
FPS_MAX = "fps_max"
config = None

def read_configuration():
    config_ini = configparser.ConfigParser(allow_unnamed_section=True)
    config_ini.read("config.ini")
    return config_ini


class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
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

        #timer to check events
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.updateUI)
        self.timer.start()

    def video_directory(self):
        global config
        global CONFIG_VIDEO_PATH
        return f"{config[configparser.UNNAMED_SECTION][CONFIG_VIDEO_PATH]}"

    def idle_video(self):
        global config
        global CONFIG_IDLE_VIDEO_NAME
        return f"{self.video_directory()}/{config[configparser.UNNAMED_SECTION][CONFIG_IDLE_VIDEO_NAME]}"

    def play_idle_video(self):
        global idle_is_playing
        if(self.mediaplayer.is_playing()):
            return
        idle_is_playing = True
        self.open_file(self.idle_video())
        return
    
    def updateUI(self):
        global requested_video_name
        global kill_process
        self.play_idle_video()
        requested_video_name = self.check_video_request()
        if requested_video_name:
            self.play_video(f"{self.video_directory()}/{requested_video_name}")
            requested_video_name = None
            return


    def check_video_request(self):
        global requested_video_name
        global CONFIG_SERVER_URL
        url = f"{config[configparser.UNNAMED_SECTION][CONFIG_SERVER_URL]}/watch"
        contents = urllib.request.urlopen(url).read()
        if contents:
            #debug(f"scanned <{contents.decode('utf-8')}>")
            return contents.decode('utf-8')
        return None

    def play_video(self, video):
        global idle_is_playing
        if (requested_video_name is not None) & (idle_is_playing == True):
            self.stop_video()
            idle_is_playing = False
            self.open_file(video)


    def open_file(self, video):
        # Open a file dialog to select a video file.
        self.filename = video
        path = Path(video)
        print(path.absolute())
        if self.filename:
            media = self.instance.media_new(path.absolute())
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

    def stop_video(self):
        self.mediaplayer.stop()

if __name__ == "__main__":
    config = read_configuration()
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec())
