#!/bin/bash

# Name of the Docker host bridge network acting as WAN
WAN_INTERFACE=eth0

# Name and IP of the internal bridge acting as LAN
LAN_BRIDGE=br_internal
LAN_IP=192.168.5.1/24

# Create LAN network bridge
brctl addbr $LAN_BRIDGE
ip addr add $LAN_IP dev $LAN_BRIDGE
ip link set dev $LAN_BRIDGE up

# Enable IP forwarding
echo 1 > /proc/sys/net/ipv4/ip_forward

# Configure NAT from LAN to WAN
iptables -t nat -A POSTROUTING -o $WAN_INTERFACE -j MASQUERADE
iptables -A FORWARD -i $LAN_BRIDGE -o $WAN_INTERFACE -j ACCEPT
iptables -A FORWARD -i $WAN_INTERFACE -o $LAN_BRIDGE -m state --state RELATED,ESTABLISHED -j ACCEPT

# Create a veth pair so application inside can talk outside
ip link add veth0 type veth peer name veth1

# Attach one end of the veth pair to br_internal
ip link set veth1 master br_internal

# Bring up both ends of the veth pair
ip link set veth0 up
ip link set veth1 up

# Assign an IP address to veth0
ip addr add 192.168.5.2/24 dev veth0

# Optional: Configure additional LAN interfaces or services here

# Run your main application or service (e.g., start a QEMU instance)
# Example: Run the QEMU simulation (adjust according to your setup)
# qemu-system-arm -machine my_board -kernel /zephyrproject/my_zephyr_app/build/zephyr/zephyr.elf -netdev bridge,id=net0,br=$LAN_BRIDGE -device my_net_device,netdev=net0

# Keep the container running so that network tools can be used interactively
# Comment or remove if your main process keeps the container alive
tail -f /dev/null