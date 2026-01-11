import configparser
import sys
from PyQt6.QtWidgets import (
    QMainWindow,
    QFrame,
    QVBoxLayout
)
from PyQt6.QtCore import QTimer, Qt, pyqtSlot
import vlc

requested_video_name = None
idle_is_playing = True
CONFIG_VIDEO_PATH = "video_folder"
CONFIG_IDLE_VIDEO_NAME = "idle_video"
FPS_MAX = "fps_max"

class VideoPlayer(QMainWindow):
    def __init__(self, config : configparser.ConfigParser):
        super().__init__()
        self.config = config
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
        print(f'Video Player playing: {filename}')

    def video_directory(self):
        global CONFIG_VIDEO_PATH
        return f"{self.config[configparser.UNNAMED_SECTION][CONFIG_VIDEO_PATH]}"

    def idle_video(self):
        global CONFIG_IDLE_VIDEO_NAME
        return f"{self.video_directory()}/{self.config[configparser.UNNAMED_SECTION][CONFIG_IDLE_VIDEO_NAME]}"

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
        server_url = f"{self.config[configparser.UNNAMED_SECTION][CONFIG_SERVER_URL]}/watch"
        try:
            contents = urllib.request.urlopen(url=server_url, timeout=5).read()
            if contents:
                #debug(f"scanned <{contents.decode('utf-8')}>")
                return contents.decode('utf-8')
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
        return None

    def play_video(self, video):
        global idle_is_playing
        if (requested_video_name is not None) & (idle_is_playing == True):
            self.stop_video()
            idle_is_playing = False
            self.open_file(video)
            self.timer.stop()
            sleep(2)
            self.timer.start()


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
