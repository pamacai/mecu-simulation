
import socket
import time

# The address of the server running on the host
host_address = ('192.168.2.26', 10000)  # Replace <host_lan_ip> with the host's LAN IP address
# Bind to this specific interface
local_bind_address = ('192.168.5.10', 0)  # Assuming this is the desired source IP

def send_message_periodically():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        # Bind the socket to a specific network interface
        sock.bind(local_bind_address)

        # Send a message every second
        while True:
            message = 'Hello, UDP Server'
            sock.sendto(message.encode(), host_address)
            print(f"Sent message to {host_address}")
            time.sleep(1)  # Wait for 1 second before sending the next message

if __name__ == "__main__":
    send_message_periodically()
