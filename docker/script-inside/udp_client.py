import socket

# Server IP, port, and message
server_address = ('192.168.5.2', 10000)
message = 'Hello, UDP Server'

# Create a UDP socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.sendto(message.encode(), server_address)
    print(f"Sent message to {server_address}")