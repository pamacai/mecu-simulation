# Testing network with one udp client and one server
## build docker images and run
docker build -f docker-file-zephyr-mecu -t  frank-qemu-simu .
docker run --privileged --name container1 -it  frank-qemu-simu bash
docker run --privileged --name container2 -it  frank-qemu-simu bash
## Test the client and server with two instances
inside docker to go to root
`python3 udp_client.py 192.168.2.26 10000 dragon`
  here, 192.168.2.26 is host ip address
        10000 is host server port
        dragon is docker container client name

In host machine which has docker interface address as 192.168.2.26
cd /home/frank_home/workspace/mecu-simulation/docker/script-inside
python3 udp_server.py

