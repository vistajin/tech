~~~sh
docker pull ubuntu

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
