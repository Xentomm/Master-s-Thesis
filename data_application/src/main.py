import sys
import os
import numpy as np
import logger
import logging
from daq import DataCollectionThread
from camera import Camera
from lepton import LeptonCamera
from datetime import datetime
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QAction, QInputDialog, QMainWindow, QMenuBar, QLineEdit, QDialog, QDialogButtonBox, QVBoxLayout, QFormLayout

class DirectoryInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Set Directory")
        self.layout = QVBoxLayout()

        self.text1 = QLineEdit(self)
        self.text2 = QLineEdit(self)
        self.text3 = QLineEdit(self)

        formLayout = QFormLayout()
        formLayout.addRow("Name:", self.text1)
        formLayout.addRow("Surname:", self.text2)
        formLayout.addRow("Age:", self.text3)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout.addLayout(formLayout)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def getInputs(self):
        return self.text1.text(), self.text2.text(), self.text3.text()

class GridExample(QMainWindow):
    def __init__(self):
        super().__init__()
        self.name = ""
        self.surname = ""
        self.age = ""
        self.saveDir = ""
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
        self.data_thread = DataCollectionThread(self.device_description, self.profile_path,
                                                self.channel_count, self.start_channel)

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
                       "Setup ActiveView.\n"
                       "Setup Directory in Menu Bar.\n"
                       "Click on Stop Plotting.\n"
                       "Press F1 to start data gathering.\n"
                       "Press F2 to stop data gathering and save.\n"
                       "\n"
                       "\n"
                       "\n"
                       "\n"
                       "Press File -> Reset in Menu Bar to restart the application.\n"
                       "Press Start Plotting to show camera feeds.\n"
                       "Press Stop Plotting to pause camera feeds.")
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
            os.makedirs(self.saveDir, exist_ok=True)
            self.textLabel1.setText(self.saveDir)

    def resetApp(self):
        logging.critical("App reset")
        self.textLabel.setText("Showing data")
        self.textLabel1.setText("Save directory: ")
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

    def stopPlots(self):
        logging.info("Plots stopped")
        self.textLabel.setText("Press F1 to start data gathering")
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

    def keyPressEvent(self, event):
        f_keys = {
        Qt.Key_F3: "F3",
        Qt.Key_F4: "F4",
        Qt.Key_F5: "F5",
        Qt.Key_F6: "F6",
        Qt.Key_F7: "F7",
        Qt.Key_F8: "F8",
        Qt.Key_F9: "F9",
        Qt.Key_F10: "F10",
        Qt.Key_F11: "F11",
        Qt.Key_F12: "F12"
    }

        if event.key() == Qt.Key_F1:
            if self.name == "":
                self.setDirectory()
            self.showCameras = False
            self.camera.gathering = True
            self.thermal_camera.gathering = True
            self.data_thread.start()
            self.textLabel.setText("Data gathering, press F2 to stop")
            self.dataStatusLabel.setText("Data Thread Status: Data gathering")
            self.startDataCollection()
        elif event.key() == Qt.Key_F2:
            self.camera.gathering = False
            self.thermal_camera.gathering = False
            self.textLabel.setText("Saving data")
            self.dataStatusLabel.setText("Saving data")
            self.cameraFeed.setPixmap(self.createPlaceholderImage("Data saving"))
            self.thermalCameraFeed.setPixmap(self.createPlaceholderImage("Data saving"))
            self.stopAndSaveData()
        elif event.key() in f_keys:
            logging.info(f"{f_keys[event.key()]} pressed")

    def startDataCollection(self):
        self.cameraFeed.setPixmap(self.createPlaceholderImage("Data gathering, press F2 to stop"))
        self.thermalCameraFeed.setPixmap(self.createPlaceholderImage("Data gathering, press F2 to stop"))

    def stopAndSaveData(self):
        self.camera.stop()
        self.thermal_camera.stop()
        self.data_thread.stop()
        cameraData = self.camera.getFrames()
        leptonData = self.thermal_camera.getFrames()
        np.savez(self.saveDir + "data.npz", cameraData=cameraData, leptonData=leptonData)

        daqData, daqData1 = self.data_thread.getData()
        daqData1.to_csv(self.saveDir + "gsr.csv", index=False)
        daqData.to_csv(self.saveDir + "ekg.csv", index = False)

        logging.info("Data saved")
        self.textLabel.setText(f"Data saved at {self.saveDir}")

    def imageUpdateSlot(self, image):
        self.cameraFeed.setPixmap(QPixmap.fromImage(image))

    def imageTUpdateSlot(self, image):
        self.thermalCameraFeed.setPixmap(QPixmap.fromImage(image))

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
    
    def log_key_pressed(self, key):
        function_keys = ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12"]
        if key in function_keys:
            logging.info(f"Function key pressed by client: {key}")

if __name__ == '__main__':
    logger.setup_logging()
    app = QApplication(sys.argv)
    ex = GridExample()
    sys.exit(app.exec_())
