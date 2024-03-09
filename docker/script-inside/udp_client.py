
import sys
import socket
import time

def send_message_periodically(server_address, server_port, client_id):
    host_address = (server_address, int(server_port))
    # local_bind_address = ('192.168.5.10', 0)  # Assuming this is the desired source IP, autogenerate source port
    local_bind_address = ('192.168.5.10', int(server_port))  # Assuming this is the desired source IP

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        # Bind the socket to a specific network interface
        sock.bind(local_bind_address)

        # Set a timeout for blocking socket operations like recvfrom
        sock.settimeout(2)  # Timeout in seconds, e.g., 5 seconds

        # Send a message every second
        cnt=0
        while True:
            message = f'Hello from client {client_id} {cnt}'
            sock.sendto(message.encode(), host_address)
            print(f"Sent message to {host_address}: {message}")

            try:
                # Attempt to receive a response within the timeout period
                data, server = sock.recvfrom(1024)  # Buffer size is 1024 bytes
                print(f"Received response from {server}: {data.decode()}")
            except socket.timeout:
                # This block is executed if no data is received before the timeout
                print("Timeout, next try")
            cnt=cnt+1
            time.sleep(1)  # Wait for 1 second before sending the next message


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python script.py <server_address> <server_port> <client_id>")
        print("Example: python3 udp_client.py 192.168.2.26 10000 dragon")
        sys.exit(1)
    elif len(sys.argv) == 2 and sys.argv[1] in ['-h', '--help']:
        print("Usage: python script.py <server_address> <server_port> <client_id>")
        sys.exit(0)

    server_address = sys.argv[1]
    server_port = sys.argv[2]
    client_id = sys.argv[3]
    send_message_periodically(server_address, server_port, client_id)