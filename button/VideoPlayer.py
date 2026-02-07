import configparser
import os
import random
import sys
from PyQt6.QtCore import (
    QTimer,
    QUrl,
    pyqtSignal,
    pyqtSlot
)

from PyQt6.QtGui import (
    QKeyEvent
)

from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QMainWindow,
    QWidget,
    QPushButton
)

from PyQt6.QtMultimedia import (
  QMediaPlayer,
  QAudioOutput,
)

from PyQt6.QtMultimediaWidgets import (
  QVideoWidget
)
#os.environ["QT_LOGGING_RULES"] = "qt.multimedia.ffmpeg.debug=false"

class VideoPlayer(QMainWindow):
    def __init__(self, config : configparser.ConfigParser, parent = None):
        super().__init__(parent = parent)

        # set up user interface
        self.videoWidget = QVideoWidget()
        self.audioOut = QAudioOutput()
        self.audioOut.setVolume(0.1)
        self.setCentralWidget(self.videoWidget)

        self.config = config
        self.section = 'video'
        self.watchKeyEvents = False
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
            self.idle = os.path.join(self.media_dir, self.idle)
        
        self.idlePlayer = QMediaPlayer()
        self.idlePlayer.setObjectName('IdlePlayer')
        self.idlePlayer.mediaStatusChanged.connect(self.mediaStatusChanged)
        self.idlePlayer.playbackStateChanged.connect(self.playbackStateChanged)
        self.idlePlayer.errorOccurred.connect(self.errorOccurred)
        self.idlePlayer.setSource(QUrl.fromLocalFile(self.idle))
        self.idlePlayer.setVideoOutput(self.videoWidget)
        self.idlePlayer.setAudioOutput(self.audioOut)
        self.idlePlayer.setLoops(QMediaPlayer.Loops.Infinite)
        self.idlePosition = -1

        self.player = QMediaPlayer()
        self.player.setObjectName('SelectedPlayer')
        self.player.mediaStatusChanged.connect(self.mediaStatusChanged)
        self.player.playbackStateChanged.connect(self.playbackStateChanged)
        self.idlePlayer.errorOccurred.connect(self.errorOccurred)
        #self.player.setSource(QUrl.fromLocalFile(self.idle))
        self.player.setVideoOutput(None)
        self.player.setAudioOutput(None)

    @pyqtSlot(str)
    def triggered(self, filename : str):
        if len(filename) > 0:
            print(f'Playing: {filename}')
        else:
            filename = random.choice(self.files)
            print(f'Randomly selecting: {filename}')
        filename = os.path.join('.', self.media_dir, filename)
        self.requested_video_name = filename
        self.player.setSource(QUrl.fromLocalFile(self.requested_video_name))
    
    def load_files(self):
        extension = '.mp4'
        files = os.listdir(self.media_dir)
        for f in files:
            if f != self.idle and f.endswith(extension):
                self.files.append(f)
        #print(f'Loaded: {self.files}')

    def keyReleaseEvent(self, e : QKeyEvent):
        super().keyReleaseEvent(e)

        if self.watchKeyEvents:
            print(e.text())
            self.triggered('')

    def playIdle(self):
        print(f'Starting playback of idle video')
        self.idlePlayer.play()

    def errorOccurred(self, error : QMediaPlayer.Error , errorString : str):
        s = ''
        print(f'VideoPlayer::errorOccurred: {error}, {errorString}')
    
    def mediaStatusChanged(self, status : QMediaPlayer.MediaStatus):
        if self.sender() == self.idlePlayer:
            pass
        elif self.sender() == self.player:
            if self.requested_video_name is not None and status == QMediaPlayer.MediaStatus.LoadedMedia:
                #print('Pausing idle player')
                self.idlePosition = self.idlePlayer.position()
                self.idlePlayer.stop()
                self.idlePlayer.setVideoOutput(None)
                self.idlePlayer.setAudioOutput(None)

        #print(f'VideoPlayer::mediaStatusChanged: {self.sender().objectName()} state changed to {status}')

    def playbackStateChanged(self, newState : QMediaPlayer.PlaybackState):
        if self.sender() == self.idlePlayer:
            if self.requested_video_name is not None and newState == QMediaPlayer.PlaybackState.StoppedState:
                self.player.setVideoOutput(self.videoWidget)
                self.player.setAudioOutput(self.audioOut)
                self.player.play()
                self.requested_video_name = None
        elif self.sender() == self.player:
            if self.requested_video_name is None and newState == QMediaPlayer.PlaybackState.StoppedState:
                self.player.setVideoOutput(None)
                self.player.setAudioOutput(None)
                self.idlePlayer.setVideoOutput(self.videoWidget)
                self.idlePlayer.setAudioOutput(self.audioOut)
                if self.idlePosition != -1:
                    self.idlePlayer.setPosition(self.idlePosition)
                self.idlePlayer.play()
        #print(f'VideoPlayer::playbackStateChanged: {self.sender().objectName()} state changed to {newState}')

if __name__ == '__main__':
    config_ini = configparser.ConfigParser(allow_unnamed_section=True)
    config_ini.read("config.ini")
    app = QApplication(sys.argv)
    w = VideoPlayer2(config_ini)
    w.watchKeyEvents = True
    #w.showFullScreen()
    w.showMaximized()
    QTimer.singleShot(0, w.playIdle)

    exit(app.exec())