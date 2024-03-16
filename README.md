# Testing network with one udp client and one server
## build docker images and run
docker build -f docker-file-zephyr-mecu -t  frank-qemu-simu .
docker run --privileged --name container1 -it  frank-qemu-simu bash
docker run --privileged --name container2 -it  frank-qemu-simu bash
## Test the client and server with two instances
### Get into docker
Get into the docker image:
Find the image id:
```
docker ps
```
Example output:
```
(base) frank_home@wonderland:~/workspace/mecu-simulation/docker$ docker ps
CONTAINER ID   IMAGE                    COMMAND                  CREATED      STATUS      PORTS     NAMES
0db016256518   frank-qemu-simulator-1   "/network_setup.sh t…"   6 days ago   Up 6 days             host5
fb8540ae3e80   frank-qemu-simulator-1   "/network_setup.sh t…"   6 days ago   Up 6 days             host2
```
To get into host5:
```
docker exec -it 9c36c8c92a4c bash
```

### Inside docker
inside docker to go to root
```
    7  ping host3.example.com
    8  python3 udp_client.py 192.168.2.26 10000 lion
```
`python3 udp_client.py 192.168.2.26 10000 dragon`
  here, 192.168.2.26 is host ip address
        10000 is host server port
        dragon is docker container client name

In host machine which has docker interface address as 192.168.2.26
cd /home/frank_home/workspace/mecu-simulation/docker/script-inside
python3 udp_server.py

