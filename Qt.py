#!/usr/bin/env python

from PyQt5 import uic, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from igraph import *

from Canvas import Canvas


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('resource/gui/GUI.ui', self)
        self.setWindowIcon(QIcon('resource/gui/icon.ico'))
        self.setWindowTitle("Network Visualization - Team Black")
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)

        self.mainLayout = self.findChild(QVBoxLayout, 'verticalLayout')
        self.canvas = Canvas(self)
        self.mainLayout.addWidget(self.canvas)
        # self.setLayout(mainLayout)
        self.infoArea = self.findChild(QVBoxLayout, 'infoArea')
        self.bindMenuActions()

    def bindMenuActions(self):
        # QMenu.File
        # Open_button
        openBtn = self.findChild(QAction, 'action_Open')
        openBtn.triggered.connect(self.openFileNameDialog)
        # Save_button
        saveBtn = self.findChild(QAction, 'action_Save')
        saveBtn.triggered.connect(self.saveFileDialog)
        # Close_button
        closeBtn = self.findChild(QAction, 'action_Close')
        closeBtn.triggered.connect(self.close)
        # QMenu.View
        # Zoom in
        self.findChild(QAction, 'actionZoom_In').triggered.connect(self.canvas.zoomInEvent)
        # Zoom out
        self.findChild(QAction, 'actionZoom_Out').triggered.connect(self.canvas.zoomOutEvent)
        # Zoom reset
        self.findChild(QAction, 'actionReset_Zoom').triggered.connect(self.canvas.zoomResetEvent)
        # QMenu.Window
        # Minimize_button
        self.findChild(QAction, 'action_Minimize').triggered.connect(self.minimizeWindow)

        # Toolbar
        # Zoom in
        zoomInBtn = self.findChild(QToolButton, 'zoom_in_btn')
        zoomInBtn.pressed.connect(self.canvas.zoomInEvent)
        # Zoom out
        zoomOutBtn = self.findChild(QToolButton, 'zoom_out_btn')
        zoomOutBtn.pressed.connect(self.canvas.zoomOutEvent)
        # Zoom reset
        zoomResetBtn = self.findChild(QToolButton, 'zoom_reset_btn')
        zoomResetBtn.pressed.connect(self.canvas.zoomResetEvent)
        # Color picker
        colorPickerBtn = self.findChild(QToolButton, 'color_picker_btn')
        colorPickerBtn.pressed.connect(self.openColorDialog)

    def openColorDialog(self):
        color = QColorDialog.getColor()

        if color.isValid():
            print(color.name())

    def minimizeWindow(self):
        if self.windowState() == Qt.WindowNoState or self.windowState() == Qt.WindowMaximized:
            # Minimize window
            self.setWindowState(Qt.WindowMinimized)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Open", "",
            "All Files (*);;Python Files (*.py)", options=options
        )
        if fileName:
            print("Open filename: " + fileName)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Save As", "",
            "All Files (*);;JPG Files (*.jpg)", options=options
        )
        if fileName:
            self.preview_screen.save(fileName, "jpg")
            # output = plot(self.result.g)
            # output.save(fileName)
            # output = QScreen.grabWindow(self.main_layout.winId())

            # output.save(fileName, format='jpg')
            # print("Save filename: " + fileName)

    def clearLayout(self, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().deleteLater()

    def displayVertex(self, l):
        # vertexInfo = VertexInfo(vertex)
        self.clearLayout(self.infoArea)
        print('abc')
        print(l)
        testLabel = QLabel("&Clicked" + str(l))
        self.infoArea.addWidget(testLabel)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
