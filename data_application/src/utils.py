from pynput.keyboard import Key, Listener
from pynput import mouse
from PyQt5 import QtCore
import logging
from PyQt5.QtWidgets import QLineEdit, QDialog, QDialogButtonBox, QFormLayout, QVBoxLayout

class KeyMonitor(QtCore.QObject):
    keyPressed = QtCore.pyqtSignal(Key)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.listener = Listener(on_release=self.on_release)
        self.mouse_listener = mouse.Listener(on_click=self.on_click)

    def on_release(self, key):
        if isinstance(key, Key):
            self.keyPressed.emit(key)   

    def stop_monitoring(self):
        self.listener.stop()
        self.mouse_listener.stop()

    def start_monitoring(self):
        self.listener.start()
        self.mouse_listener.start()

    def on_click(self, x, y, button, pressed):
        if pressed:
            # print('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))
            logging.critical("Mouse pressed FLAG MOVE")



def PressedKey(key, grid_instance):
    if key == Key.f1 and grid_instance.gathering == False:
        logging.critical(f"Pressed {key} FLAG DATA START")
        grid_instance.gathering = True
        grid_instance.showCameras = False
        grid_instance.camera.gathering = True
        # grid_instance.thermal_camera.gathering = True
        # grid_instance.data_thread.start()
        grid_instance.textLabel.setText("Data gathering, press F1 to stop")
        grid_instance.dataStatusLabel.setText("Data Thread Status: Data gathering")
        grid_instance.startDataCollection()
    elif key == Key.f1 and grid_instance.gathering == True:
        logging.critical(f"Pressed {key} FLAG DATA STOPPED")
        grid_instance.camera.gathering = False
        # grid_instance.thermal_camera.gathering = False
        grid_instance.textLabel.setText("Saving data")
        grid_instance.dataStatusLabel.setText("Saving data")
        grid_instance.cameraFeed.setPixmap(grid_instance.createPlaceholderImage("Data saving"))
        # grid_instance.thermalCameraFeed.setPixmap(grid_instance.createPlaceholderImage("Data saving"))
        grid_instance.stopAndSaveData()
    elif key == Key.f6:
        logging.critical(f"Pressed {key} FLAG ... ")
    elif key == Key.f7:
        logging.critical(f"Pressed {key} FLAG ... ")
    elif key == Key.f8:
        logging.critical(f"Pressed {key} FLAG ... ")
    else:
        pass

def mouse_clicked():
    pass


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