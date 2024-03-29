import socket

# Server IP and port
server_address = ('0.0.0.0', 10000)

# Create a UDP socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.bind(server_address)
    print("UDP server listening on", server_address)

    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Received message: {data.decode()} from {addr}")

        # Echo back the received message
        sock.sendto(data, addr)
        print(f"Echoed back message to {addr}")