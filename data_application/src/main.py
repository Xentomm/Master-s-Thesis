import sys
import numpy as np
import pyqtgraph as pg
from camera import Camera
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QHBoxLayout, QVBoxLayout, QLabel

class GridExample(QWidget):
    def __init__(self):
        super().__init__()
        self.gathering = False
        self.showCameras = True
        self.camera = Camera()
        self.camera.imageUpdate.connect(self.imageUpdateSlot)
        self.camera.start()

        self.initUI()

    def initUI(self):
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)
        
        grid = QGridLayout()
        mainLayout.addLayout(grid)

        plotGsr = pg.PlotWidget()
        plotEkg = pg.PlotWidget()

        self.cameraFeed = QLabel()
        self.thermalCameraFeed = QLabel()

        self.placeholderImage = self.createPlaceholderImage("Data coming soon")
        self.cameraFeed.setPixmap(self.placeholderImage)
        self.thermalCameraFeed.setPixmap(self.placeholderImage)

        grid.addWidget(plotGsr, 0, 0)
        grid.addWidget(plotEkg, 1, 0)
        grid.addWidget(self.cameraFeed, 0, 1)
        grid.addWidget(self.thermalCameraFeed, 1, 1)

        textLayout = QHBoxLayout()
        self.textLabel = QLabel("Showing data")
        self.textLabel.setAlignment(Qt.AlignCenter)
        textLayout.addWidget(self.textLabel)
        mainLayout.addLayout(textLayout)

        buttonLayout = QHBoxLayout()
        mainLayout.addLayout(buttonLayout)

        startButton = QPushButton('Stop Plotting')
        startButton.setFixedSize(100, 50)
        startButton.clicked.connect(self.stopPlots)
        buttonLayout.addWidget(startButton)

        stopButton = QPushButton('Start Plotting')
        stopButton.setFixedSize(100, 50)
        stopButton.clicked.connect(self.startPlots)
        buttonLayout.addWidget(stopButton)

        resetButton = QPushButton('Reset')
        resetButton.setFixedSize(100, 50)
        resetButton.clicked.connect(self.resetApp)
        buttonLayout.addWidget(resetButton)

        self.setWindowTitle('Data Application')
        self.setGeometry(50, 50, 1600, 800)
        self.show()

    def resetApp(self):
        self.textLabel.setText("Showing data")
        self.showCameras = True
        self.camera.start()
        self.updateCameraConnection()
        self.camera.frames = []

    def stopPlots(self):
        self.textLabel.setText("Press F1 to start data gathering")
        self.showCameras = False
        self.updateCameraConnection()

    def startPlots(self):
        self.textLabel.setText("Showing data")
        self.showCameras = True
        self.updateCameraConnection()

    def updateCameraConnection(self):
        if self.showCameras:
            self.camera.imageUpdate.connect(self.imageUpdateSlot)
        else:
            self.camera.imageUpdate.disconnect(self.imageUpdateSlot)
            self.cameraFeed.setPixmap(self.placeholderImage)
            self.thermalCameraFeed.setPixmap(self.placeholderImage)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F1:
            self.showCameras = False
            self.camera.gathering = True
            self.textLabel.setText("Data gathering, press F2 to stop")
            self.startDataCollection()
        elif event.key() == Qt.Key_F2:
            self.camera.gathering = False
            self.textLabel.setText("Saving data")
            self.cameraFeed.setPixmap(self.createPlaceholderImage("Data saving"))
            self.thermalCameraFeed.setPixmap(self.createPlaceholderImage("Data saving"))
            self.stopAndSaveData()

    def startDataCollection(self):
        self.cameraFeed.setPixmap(self.createPlaceholderImage("Data gathering, press F2 to stop"))
        self.thermalCameraFeed.setPixmap(self.createPlaceholderImage("Data gathering, press F2 to stop"))

    def stopAndSaveData(self):
        self.camera.stop()
        cameraData = self.camera.getFrames()
        saveDir = "data_application/collected/gathered_data.npz"
        np.savez(saveDir, cameraData=cameraData)
        self.textLabel.setText(f"Data saved at {saveDir}")
        # print("Data saved to gathered_data.npz")

    def imageUpdateSlot(self, image):
        self.cameraFeed.setPixmap(QPixmap.fromImage(image))

    def createPlaceholderImage(self, text):
        image = QPixmap(500, 380)
        image.fill(Qt.gray)

        painter = QPainter(image)
        painter.setPen(Qt.white)
        font = QFont("Arial", 16)
        painter.setFont(font)
        textRect = painter.boundingRect(image.rect(), Qt.AlignCenter, text)
        painter.drawText(textRect, Qt.AlignCenter, text)
        painter.end()

        return image

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GridExample()
    sys.exit(app.exec_())
