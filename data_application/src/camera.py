import cv2
import numpy as np
from PyQt5.QtGui import QImage
from PyQt5.QtCore import QThread, pyqtSignal, Qt

class Camera(QThread):
    imageUpdate = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.frames = []
        self.gathering = False
    
    def run(self):
        self.threadActive = True
        capture = cv2.VideoCapture(0)
        while self.threadActive:
            ret, frame = capture.read()
            if ret:
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                flippedImage = cv2.flip(image, 1)
                convert2qt = QImage(flippedImage.data, flippedImage.shape[1], flippedImage.shape[0], QImage.Format_RGB888)
                pic = convert2qt.scaled(500, 400, Qt.KeepAspectRatio)
                self.imageUpdate.emit(pic)
                if self.gathering:
                    self.frames.append(frame)

    def stop(self):
        self.threadActive = False
        self.quit()

    def getFrames(self):
        return np.array(self.frames)