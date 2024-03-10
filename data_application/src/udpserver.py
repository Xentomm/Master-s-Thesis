# from PyQt5.QtCore import pyqtSignal, QThread
# import socket
# from utils import read_config

# class UDPServer(QThread):
#     key_pressed = pyqtSignal(str)

#     def __init__(self, parent=None):
#         super().__init__(parent)
#         config = read_config('data_application/src/config.json')
#         self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         self.socket.bind((config['server_ip'], config['server_port']))

#     def run(self):
#         while True:
#             data, addr = self.socket.recvfrom(1024)
#             message = data.decode('utf-8')
#             self.key_pressed.emit(message)