from PyQt5.QtCore import QPropertyAnimation, QPointF, QUrl
from PyQt5.QtGui import QIcon, QPainterPath, QMovie
from PyQt5.QtWidgets import QDialog, QLabel
from PyQt5.uic import loadUi
from PyQt5.QtMultimedia import *


class AboutUsDialog(QDialog):
    def __init__(self):
        super().__init__()

        loadUi('resource/gui/AboutUsDialog.ui', self)
        self.setWindowIcon(QIcon('resource/gui/icon.ico'))
        self.setWindowTitle("About Us")
        self.media = QMediaPlaylist()
        url = QUrl.fromLocalFile('resource/media/music.mp3')
        self.media.addMedia(QMediaContent(url))
        self.media.setPlaybackMode(QMediaPlaylist.Loop)

        self.player = QMediaPlayer()
        self.player.setPlaylist(self.media)
        self.player.play()

        self.mascot = self.findChild(QLabel, 'mascotLabel')
        self.mascotFlip = self.findChild(QLabel, 'mascotLabel2')
        self.mascotGif = QMovie("resource/image/small-mascot.gif")
        self.mascotGif2 = QMovie("resource/image/small-mascot-flip.gif")
        self.mascot.setMovie(self.mascotGif)
        self.mascotFlip.setMovie(self.mascotGif2)
        self.anim2 = QPropertyAnimation(self.mascotFlip, b"pos")
        self.anim = QPropertyAnimation(self.mascot, b"pos")

        self.step = 10
        self.xRange = 500
        self.duration = 5000
        try:
            self.goOn()
        except Exception as e:
            print(e)

    def goOn(self):
        self.mascotFlip.hide()
        self.mascotGif.start()
        self.mascot.show()
        path = QPainterPath()
        path.moveTo(-70, 410)
        for i in range(self.step):
            path.quadTo(QPointF(self.xRange / self.step * i - 70 + (self.xRange / self.step / 2), 390),
                        QPointF((self.xRange / self.step) * i - 70 + (self.xRange / self.step), 410))
        vals = [p / 100 for p in range(0, 101)]
        self.anim.setDuration(self.duration)
        for i in vals:
            self.anim.setKeyValueAt(i, path.pointAtPercent(i))
        self.anim.start()
        self.anim.finished.connect(self.goFlip)

    def goFlip(self):
        self.mascot.hide()
        self.mascotGif2.start()
        self.mascotFlip.show()
        path2 = QPainterPath()
        path2.moveTo(500, 410)
        for i in range(self.step):
            path2.quadTo(QPointF(500 - (self.xRange / self.step) * i - (self.xRange / self.step / 2), 390),
                         QPointF(500 - (self.xRange / self.step) * i - (self.xRange / self.step), 410))
        vals = [p / 100 for p in range(0, 101)]
        self.anim2.setDuration(self.duration)
        for i in vals:
            self.anim2.setKeyValueAt(i, path2.pointAtPercent(i))
        self.anim2.start()
        self.anim2.finished.connect(self.goOn)
