import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFileDialog
)
from PyQt6.QtCore import QTimer, Qt
import vlc

class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 VLC Media Player")
        self.setGeometry(100, 100, 800, 600)

        self.filename = ""

        # Create a VLC instance and a media player.
        self.instance = vlc.Instance()
        self.mediaplayer = self.instance.media_player_new()

        # Set up the main widget and layout.
        self.widget = QFrame(self)
        self.setCentralWidget(self.widget)
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)

        # Create the video frame where VLC will render the video.
        self.video_frame = QFrame()
        self.video_frame.setStyleSheet("background: black;")
        self.layout.addWidget(self.video_frame)

        # Create a horizontal layout for control buttons and progress slider.
        self.controls_layout = QHBoxLayout()
        self.layout.addLayout(self.controls_layout)

        # Open button: Open a video file.
        self.open_button = QPushButton("Open Video")
        self.open_button.clicked.connect(self.open_file)
        self.controls_layout.addWidget(self.open_button)

    def open_file(self):
        # Open a file dialog to select a video file.
        self.filename, _ = QFileDialog.getOpenFileName(self, "Open Video")
        if self.filename:
            media = self.instance.media_new(self.filename)
            self.mediaplayer.set_media(media)
            # Embed the VLC video output into our video frame.
            if sys.platform.startswith('linux'):
                self.mediaplayer.set_xwindow(int(self.video_frame.winId()))
            elif sys.platform == "win32":
                self.mediaplayer.set_hwnd(self.video_frame.winId())
            elif sys.platform == "darwin":
                self.mediaplayer.set_nsobject(int(self.video_frame.winId()))
            self.mediaplayer.play()

    def pause_video(self):
        # Pause or resume video playback.
        self.mediaplayer.pause()

    def stop_video(self):
        self.mediaplayer.stop()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec())
