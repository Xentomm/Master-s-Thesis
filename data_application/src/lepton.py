import numpy as np
from flirpy.camera.lepton import Lepton
from PyQt5.QtGui import QImage
from PyQt5.QtCore import QThread, pyqtSignal

class LeptonCamera(QThread):
    imageUpdate = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.frames = []
        self.gathering = False

    def run(self):
        self.threadActive = True
        with Lepton() as l:
            while self.threadActive:
                frame = l.grab().astype(np.float32)
                frame = (frame / frame.max()) * 255.0
                frame = frame.astype(np.uint8)
                if frame is not None:
                    self.frames.append(frame)
                    self.imageUpdate.emit(self.convertFrameToQImage(frame))
                    if self.gathering:
                        self.frames.append(frame)

    def stop(self):
        self.threadActive = False
        self.quit()

    def getFrames(self):
        return np.array(self.frames)

    def convertFrameToQImage(self, frame):
        height, width = frame.shape
        bytesPerLine = width
        image = QImage(frame.data, width, height, bytesPerLine, QImage.Format_Grayscale8)
        image = image.convertToFormat(QImage.Format_RGB888)
        return image
