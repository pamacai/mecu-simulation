# Testing network with udp client and server
## build docker images and run
docker build -f docker-file-zephyr-mecu -t  frank-qemu-simu .
docker run --privileged --name container1 -it  frank-qemu-simu bash
docker run --privileged --name container2 -it  frank-qemu-simu bash
## Test the client and server with two instances
inside docker to go to root
python3 udp_client.py

In host machine which has docker interface address as 192.168.2.26
cd /home/frank_home/workspace/mecu-simulation/docker/script-inside
python3 udp_server.py

