import sys
from PyQt6.QtCore import (
    QUrl,
    pyqtSignal
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

class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent = parent)

        self.container = QWidget()
        l = QVBoxLayout()
        self.container.setLayout(l)
        self.videoWidget = QVideoWidget()
        self.audioOut = QAudioOutput()
        l.addWidget(self.videoWidget)
        self.pushButton = QPushButton('Play')
        self.pushButton.clicked.connect(self.togglePlayer)
        l.addWidget(self.pushButton)
        self.setCentralWidget(self.container)
        
        self.player = QMediaPlayer()
        self.player.setSource(QUrl.fromLocalFile('/Users/sean/Documents/Fortress Party/vault_of_midnight/button/media/video/idle.mp4'))
        self.player.setVideoOutput(self.videoWidget)
        self.player.setAudioOutput(self.audioOut)
        self.audioOut.setVolume(1.0)

    def togglePlayer(self):
        if self.player.isPlaying():
            print('Stopping')
            self.player.stop()
        else:
            print('Playing')
            self.player.play()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.showFullScreen()
    exit(app.exec())