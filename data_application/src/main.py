import sys
import os
import numpy as np
import logger
import logging
from utils import KeyMonitor, PressedKey, DirectoryInputDialog
from daq import DataCollectionThread
from camera import Camera
from lepton import LeptonCamera
from datetime import datetime
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QAction, QMainWindow, QVBoxLayout

class GridExample(QMainWindow):
    def __init__(self):
        super().__init__()
        self.name = ""
        self.surname = ""
        self.age = ""
        self.saveDir = ""
        self.textLabel1 = QLabel(f"Save directory: {self.saveDir}")
        self.gathering = False
        self.showCameras = True
        self.camera = Camera()
        self.thermal_camera = LeptonCamera()
        self.camera.imageUpdate.connect(self.imageUpdateSlot)
        self.thermal_camera.imageUpdate.connect(self.imageTUpdateSlot)
        self.camera.start()
        self.thermal_camera.start()

        self.device_description = "USB-4716,BID#0"
        self.profile_path = "../../profile/DemoDevice.xml"
        self.channel_count = 2
        self.start_channel = 0
        self.data_thread = None
        
        self.monitor = KeyMonitor()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')

        resetAction = QAction('&Reset', self)
        resetAction.triggered.connect(self.resetApp)
        fileMenu.addAction(resetAction)

        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)

        dirMenu = menubar.addMenu('&Directory')

        setDirAction = QAction('&Set Directory', self)
        setDirAction.triggered.connect(self.setDirectory)
        dirMenu.addAction(setDirAction)

        self.initUI()

    def initUI(self):
        logging.critical('Start')
        mainLayout = QVBoxLayout()
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        centralWidget.setLayout(mainLayout)
        
        grid = QGridLayout()
        mainLayout.addLayout(grid)

        infoLabel = QLabel("Instructions:\n\n"
                       "Watch camera feed and setup them correctly.\n"
                       "Launch ActiveView.\n"
                       "Setup Directory in Menu Bar.\n"
                       "Click on Stop Plotting.\n"
                       "Start ActiView file in the same directory.\n"
                       "Press F1 to start data gathering.\n"
                       "Press F1 to stop data gathering and save.\n"
                       "\n"
                       "\n"
                       "Use these to flag the game:\n"
                       "F6 -> new deal\n"
                       "F7 -> ...\n"
                       "F8 -> ...\n"
                       "\n"
                       "\n"
                       "Press File -> Reset in Menu Bar to restart the application.\n"
                       "Or restart the app by exiting")
        infoLabel.setAlignment(Qt.AlignCenter)
        
        self.dataStatusLabel = QLabel("Data Thread Status: Idle")
        self.dataStatusLabel.setAlignment(Qt.AlignCenter)

        self.cameraFeed = QLabel()
        self.thermalCameraFeed = QLabel()

        self.placeholderImage = self.createPlaceholderImage("Data coming soon")
        self.cameraFeed.setPixmap(self.placeholderImage)
        self.thermalCameraFeed.setPixmap(self.placeholderImage)

        grid.addWidget(infoLabel, 0, 0)
        grid.addWidget(self.dataStatusLabel, 1, 0)
        grid.addWidget(self.cameraFeed, 0, 1)
        grid.addWidget(self.thermalCameraFeed, 1, 1)

        textLayout = QVBoxLayout()
        self.textLabel = QLabel("Showing data")
        self.textLabel.setAlignment(Qt.AlignCenter)
        textLayout.addWidget(self.textLabel)
        mainLayout.addLayout(textLayout)

        textLayout1 = QVBoxLayout()
        self.textLabel1 = QLabel(f"Save directory: ")
        self.textLabel1.setAlignment(Qt.AlignCenter)
        textLayout.addWidget(self.textLabel1)
        mainLayout.addLayout(textLayout1)

        buttonLayout = QHBoxLayout()
        mainLayout.addLayout(buttonLayout)

        startButton = QPushButton('Start Plotting')
        startButton.setFixedSize(100, 50)
        startButton.clicked.connect(self.startPlots)
        buttonLayout.addWidget(startButton)

        stopButton = QPushButton('Stop Plotting')
        stopButton.setFixedSize(100, 50)
        stopButton.clicked.connect(self.stopPlots)
        buttonLayout.addWidget(stopButton)

        self.setWindowTitle('Data Application')
        self.setGeometry(0, 0, 990, 1010)
        self.show()

    def setDirectory(self):
        dialog = DirectoryInputDialog()
        if dialog.exec_():
            self.name, self.surname, self.age = dialog.getInputs()
            current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            self.saveDir = f"data_application/collected/{current_datetime}_{self.name[0]}{self.surname[0]}{self.age}/"
            logging.info(f"Save dir: {self.saveDir}")
            logging.info(f"Patient Data: {self.name}, {self.surname}, {self.age}")
            os.makedirs(self.saveDir, exist_ok=True)
            self.textLabel1.setText(self.saveDir)
            self.textLabel.setText("Press F1 to start gathering data")
        self.monitor.keyPressed.connect(lambda key: PressedKey(key, self))
        self.monitor.start_monitoring()
        self.data_thread = DataCollectionThread(self.device_description, self.profile_path,
                                                self.channel_count, self.start_channel, self.saveDir)

    def resetApp(self):
        logging.critical("App reset")
        self.textLabel.setText("Showing data")
        self.textLabel1.setText("Save directory: ")
        self.monitor.stop_monitoring()
        self.monitor = KeyMonitor()
        self.showCameras = True
        self.camera.start()
        self.thermal_camera.start()
        self.updateCameraConnection()
        self.camera.frames = []
        self.thermal_camera.frames = []
        self.control = ""
        self.name = ""
        self.surname = ""
        self.age = ""
        self.saveDir = ""
        self.gathering = False

    def stopPlots(self):
        logging.info("Plots stopped")
        self.textLabel.setText("Setup directory")
        self.showCameras = False
        self.updateCameraConnection()

    def startPlots(self):
        logging.info("Plots started")
        self.textLabel.setText("Showing data")
        self.showCameras = True
        self.updateCameraConnection()

    def updateCameraConnection(self):
        if self.showCameras:
            logging.info("Cameras connect update")
            self.camera.imageUpdate.connect(self.imageUpdateSlot)
            self.thermal_camera.imageUpdate.connect(self.imageTUpdateSlot)
        else:
            logging.info("Cameras disconnect update")
            self.camera.imageUpdate.disconnect(self.imageUpdateSlot)
            self.thermal_camera.imageUpdate.disconnect(self.imageTUpdateSlot)
            self.cameraFeed.setPixmap(self.placeholderImage)
            self.thermalCameraFeed.setPixmap(self.placeholderImage)

    def startDataCollection(self):
        logging.info("Data Collection Started")
        self.cameraFeed.setPixmap(self.createPlaceholderImage("Data gathering, press F1 to stop"))
        self.thermalCameraFeed.setPixmap(self.createPlaceholderImage("Data gathering, press F1 to stop"))

    def stopAndSaveData(self):
        self.gathering = False
        self.camera.stop()
        self.thermal_camera.stop()
        self.data_thread.stop()
        cameraData = self.camera.getFrames()
        leptonData = self.thermal_camera.getFrames()
        np.savez(self.saveDir + "data.npz", cameraData=cameraData, leptonData=leptonData)
        # np.savez(self.saveDir + "data.npz", cameraData=cameraData)

        logging.info("Data saved")
        self.textLabel.setText(f"Data saved at {self.saveDir}")

    def imageUpdateSlot(self, image):
        self.cameraFeed.setPixmap(QPixmap.fromImage(image))

    def imageTUpdateSlot(self, image):
        self.thermalCameraFeed.setPixmap(QPixmap.fromImage(image))
        # pass

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
    logger.setup_logging()
    app = QApplication(sys.argv)
    ex = GridExample()
    sys.exit(app.exec_())
