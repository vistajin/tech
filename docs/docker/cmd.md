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

3. import from local template
Template online: https://wiki.openvz.org/Download/template/precreated

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
