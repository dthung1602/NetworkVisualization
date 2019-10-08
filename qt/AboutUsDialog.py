from PyQt5.QtCore import QPropertyAnimation, QRect, QPointF
from PyQt5.QtGui import QIcon, QPainterPath
from PyQt5.QtWidgets import QDialog, QLabel
from PyQt5.uic import loadUi


class AboutUsDialog(QDialog):
    def __init__(self):
        super().__init__()

        loadUi('resource/gui/AboutUsDialog.ui', self)
        self.setWindowIcon(QIcon('resource/gui/icon.ico'))
        self.setWindowTitle("About Us")

        self.mascot = self.findChild(QLabel, 'mascotLabel')
        self.mascotFlip = self.findChild(QLabel, 'mascotLabel2')
        self.anim2 = QPropertyAnimation(self.mascotFlip, b"pos")
        self.anim = QPropertyAnimation(self.mascot, b"pos")

        self.step = 10
        self.xRange = 500

        self.goOn()


    def goOn(self):
        self.mascotFlip.hide()
        self.mascot.show()
        path = QPainterPath()
        path.moveTo(-70, 410)
        for i in range(self.step):
            path.quadTo(QPointF(self.xRange / self.step * i - 70 + (self.xRange / self.step / 2), 370),
                        QPointF((self.xRange / self.step) * i - 70 + (self.xRange / self.step), 410))
        vals = [p / 100 for p in range(0, 101)]
        self.anim.setDuration(5000)
        for i in vals:
            self.anim.setKeyValueAt(i, path.pointAtPercent(i))
        self.anim.start()
        self.anim.finished.connect(self.goFlip)

    def goFlip(self):
        self.mascot.hide()
        self.mascotFlip.show()
        path2 = QPainterPath()
        path2.moveTo(500, 410)
        for i in range(self.step):
            path2.quadTo(QPointF(500 - (self.xRange / self.step) * i - (self.xRange / self.step / 2), 370),
                         QPointF(500 - (self.xRange / self.step) * i - (self.xRange / self.step), 410))
        vals = [p / 100 for p in range(0, 101)]
        self.anim2.setDuration(5000)
        for i in vals:
            self.anim2.setKeyValueAt(i, path2.pointAtPercent(i))
        self.anim2.start()
        self.anim2.finished.connect(self.goOn)
