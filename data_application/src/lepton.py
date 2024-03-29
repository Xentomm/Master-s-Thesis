import cv2
import numpy as np
import time
from flirpy.camera.lepton import Lepton
from PyQt5.QtGui import QImage
from PyQt5.QtCore import QThread, pyqtSignal, Qt

class LeptonCamera(QThread):
    imageUpdate = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.frames = []
        self.gathering = False

    def run(self):
        self.threadActive = True
        with Lepton() as l:
            last_capture_time = time.time()
            while self.threadActive:
                frame = l.grab().astype(np.float32)
                frame = 255*(frame - frame.min())/(frame.max() - frame.min())
                frame = frame.astype(np.uint8)
                frame_interval = 1 / 3  # 3 frames per second
                if frame is not None:
                    current_time = time.time()
                    if current_time - last_capture_time >= frame_interval:
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