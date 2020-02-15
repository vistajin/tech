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

### Run Image
~~~sh
sudo docker run -ti ubuntu:latest /bin/bash
root@f3a357dec9d9:/# mkdir test
root@f3a357dec9d9:/# touch abc.txt
root@f3a357dec9d9:/# exit
~~~

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
Step 2/4 : MAINTAINER VistaJIN
 ---> Running in 2ee367968a5e
Removing intermediate container 2ee367968a5e
 ---> 82ca0e88781a
Step 3/4 : RUN touch abc.txt
 ---> Running in 95ee6e52dbf6
Removing intermediate container 95ee6e52dbf6
 ---> ce2b56a9cb25
Step 4/4 : RUN mkdir newfolder
 ---> Running in c6050159b181
Removing intermediate container c6050159b181
 ---> b37c19d35054
Successfully built b37c19d35054
Successfully tagged ubuntu2:latest
~~~

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
k8s.gcr.io/pause    3.1                 da86e6ba6ca1        2 years ago         742kB
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

### XXXX
~~~sh
docker run <image>
docker start <name|id>
docker stop <name|id>
docker ps [-a include stopped containers]
docker rm <name|id>

docker run -d --name web1 -p 8081:80 tutum/hello-world
docker stop web1
docker start web1

docker build -t xxx/xxx .
docker push xxx
~~~