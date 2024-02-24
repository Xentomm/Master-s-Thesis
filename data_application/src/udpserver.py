from PyQt5.QtCore import pyqtSignal, QThread
import socket

class UDPServer(QThread):
    key_pressed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('0.0.0.0', 9999))

    def run(self):
        while True:
            data, addr = self.socket.recvfrom(1024)
            message = data.decode('utf-8')
            self.key_pressed.emit(message)