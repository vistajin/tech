### Search Image
~~~sh
sudo docker search ansible --filter=is-automated=true -f=stars=100 --no-trunc --limit 2
~~~

### Pull Image
~~~sh
docker pull ubuntu
~~~

### List Images
~~~sh
sudo docker images
~~~

### Run Image - Create container
~~~sh
sudo docker run -ti ubuntu:latest /bin/bash
root@f3a357dec9d9:/# mkdir test
root@f3a357dec9d9:/# touch abc.txt
root@f3a357dec9d9:/# exit
=====
docker run -itd --name=mycentos centos:7
-i :表示以交互模式运行容器(让容器的标准输入保持打开)
-d:表示后台运行容器,并返回容器ID
-t:为容器重新分配一个伪输入终端--name:为容器指定名称
~~~

### Show all containers
~~~sh
sudo docker ps -a
docker ps -a --format="table {{.Names}}\t{{.Image}}\t{{.Ports}}"
~~~

### Show running containers
~~~sh
sudo docker ps
~~~

### Stop container
~~~sh
sudo docker stop CONTAINER_ID / CONTAINER_NAME
~~~

### Stop all containers
~~~sh
docker stop $(docker ps -a -q)
~~~

### Start container
~~~sh
sudo docker start CONTAINER_ID / NAME
~~~

### Restart container
~~~sh
sodu docker restart CONTAINER_ID / NAME
~~~

### Delete container
~~~sh
sudo docker rm CONTAINER_ID / NAME
~~~

### Force delete container
~~~sh
sudo docker rm -f CONTAINER_ID / NAME
~~~

### Check container info (such as the container's IP address)
~~~sh
sudo docker inspect CONTAINER_ID / NAME
~~~

### Enter container
~~~sh
sudo docker exec -it CONTAINER_ID / NAME /bin/sh
~~~

### Copy file from host to container
~~~sh
sudo docker cp /path/to/host/file.txt CONTAINER_NAME:/path/to/container
~~~

### Copy file from container to host
~~~sh
sudo docker cp CONTAINER_NAME:/path/to/container/file.txt /path/to/host
~~~

### Attach file to container (sync file in between, changes in either side will be applied to the other)
~~~sh
sudo docker run -it -v /path/to/host/:/path/to/container iamge:tag --name <container_1>
sudo docker run -it --volumns-from <container_1> iamge:tag --name <container_2>
~~~
Tips: use docker inspect to check "Mounts", destination is container path, source is host path
Tips: in dockerfile, use VOLUME ["/path/to/container"], in this way, the post path (source) is not modifiable.

### Create Image
1. modify based on existing (container -> image)
~~~sh
sudo docker commit -m "this is a test only" -a "Vista JIN" f3a357dec9d9 ubutu:8888
sha256:4d6b039199a1d2e3f10015e72a89305094213790e90fd2ae1b73721104944a63

sudo docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
ubutu               8888                4d6b039199a1        36 seconds ago      64.2MB
ubuntu              latest              ccc6e87d482b        3 weeks ago         64.2MB
~~~
2. user Dockerfile
~~~sh
cd /
mkdir test
cd test
nano Dockerfile
----------
FROM ubuntu:8888
MAINTAINER VistaJIN
RUN touch abc.txt
RUN mkdir newfolder
.....
----------
sudo docker build -t "ubuntu2" .
Sending build context to Docker daemon   76.3MB
Step 1/4 : FROM ubutu:8888
 ---> 4d6b039199a1
.......
Removing intermediate container c6050159b181
 ---> b37c19d35054
Successfully built b37c19d35054
Successfully tagged ubuntu2:latest
~~~
#### Note: show docker build history:
~~~sh
sudo docker history name:tag
~~~

#### Dockerfile Syntax
https://docs.docker.com/engine/reference/builder/
FROM       - Base image
MAINTAINER - Author
COPY       - Copy file from host to container, the path is relative path of current Dockerfile
ADD        - COPY and then extract if the file is .tar.gz
WORKDIR    - Set current working dir
ENV        - Set environment variable
EXPOSE     - Expose container port
RUN        - Execute when build image
ENTRYPOINT - Execute when run container, when more than one, only execute the last one.
CMD        - Execute when run container, when more than one, only execute the last one. Can be overrided by parameter


3. import from local template
Template online: https://wiki.openvz.org/Download/template/precreated
~~~sh
wget http://download.openvz.org/template/precreated/contrib/oracle-7-x86_64-minimal-20170709.tar.xz
cat oracle-7-x86_64-minimal-20170709.tar.xz | sudo docker import - oracle:7
sha256:210e38f6023d030c61e0c72553bb7a30075407b1c8bbd4570886e2a0df10fe3d
sudo docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
oracle              7                   210e38f6023d        10 seconds ago      417MB
ubutu               8888                4d6b039199a1        23 hours ago        64.2MB
ubuntu              latest              ccc6e87d482b        3 weeks ago         64.2MB
hello-world         latest              fce289e99eb9        13 months ago       1.84kB
~~~

### Delete Image
~~~sh
sudo docker rmi ubutu:8888
~~~

### Save/Backup Image
~~~sh
sudo docker save -o hello-world.tar hello-world:latest
------------------------------------------------------
-rw-------  1 root     root        12800 2月  13 15:23 hello-world.tar
~~~

### Load Image
~~~sh
sudo docker load -i hello-world.tar
~~~

### Login Docker Hub
```sh
sudo docker login
..........
Login Succeeded
```
### Tag an Image
```sh
sudo docker tag fce2 vistajin/hello:first

sudo docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
hello-world         latest              fce289e99eb9        13 months ago       1.84kB
vistajin/hello      first               fce289e99eb9        13 months ago       1.84kB
```
### Create Local Repository & Upload Image
```sh
sudo docker pull registry
docker run -d -v /registry:/home/docker-registry -p 5000:5000 --restart=always --privileged=true --name registry registry:latest
sudo docker tag hello-world:latest localhost:5000/hello-world:latest
sudo docker push localhost:5000/hello-world
curl http://localhost:5000/v2/_catalog
{"repositories":["hello-world"]}
```

### Upload Image to Docker Hub
```sh
sudo docker push vistajin/hello:first
```
#### note: don't know why it hits connection reset by peer if use proxy.

### Show containers
```sh
sudo docker ps -a
```

### Start a stopped container
```sh
sudo docker start <first-4-digits-container-id>
```

### Run container in background
```sh
sudo docker run -d -c "command"
```

### Run container with super root mode (can run systemctl)
```sh
sudo docer run --priviledged=true ...
```

### Show container log
```sh
sudo docker logs <first-4-digits-container-id>
```


### Make an image with JAVA environment (with Tomcat)
~~~
FROM ubuntu:latest
ADD jdk-8u211-linux-x64.tar.gz /usr/local
RUN mv /usr/local/jdk1.8.0_211 /usr/local/jdk
ENV JAVA_HOME=/usr/local/jdk
ENV JRE_HOME=$JAVA_HOME/jre
ENV CLASSPATH=$JAVA_HOME/lib:$JRE_HOME/lib:$CLASSPATH
ENV PATH=$JAVA_HOME/bin:$JRE_HOME/bin:$PATH
ADD apache-tomcat-8.5.35.tar.gz /usr/local
RUN mv /usr/local/apache-tomcat-8.5.35 /usr/local/tomcat
EXPOSE 8080
ENTRYPOINT ["/usr/local/tomcat/bin/catalina.sh","run"]
~~~
Build:
```sh
sudo docker build -t myubuntu:java-dev .
```
Start container
~~~sh
sudo docker run -itd -p 9080:8080 -v /home/vistajin/baidunetdiskdownload/test:/usr/local/tomcat/webapps/ROOT myubuntu:java-dev /bin/bash
nano /home/vistajin/baidunetdiskdownload/test/index.html
~~~
Test: http://localhost:9080/



### Create network mode
```sh
sudo docker network create -d bridge <bridge_name>
```

### Show network mode
```sh
sudo docker network ls
```

### Connect container with bridge
```sh
sudo docker network connect <bridge_name> <container_1>
sudo docker network connect <bridge_name> <container_2>
```
Then container_1 can access container_2 and vervise.

### Start container in host mode
```sh
sudo docker run --net=host ....
```

### Link to another container
```sh
sudo docker run --link <another_container_name>
```
Benefit: don't need to care about what is the IP of another container, current container can access another container by its name

