1. ## Unable to start-up daemon
| Error | 
| :--- |
|12月 29 20:28:10 xxx-pc systemd[1]: Stopped Docker Application Container Engine.|
|12月 29 20:28:10 xxx-pc systemd[1]: Dependency failed for Docker Application Container Engine.|
12月 29 20:28:10 xxx-pc systemd[1]: docker.service: Job docker.service/start failed with result 'dependency'.|

#### Command to locate cause:
~~~sh
journalctl -u docker.service
~~~
| Log | 
| :--- |
|12月 29 20:28:10 xxx-pc dockerd[31513]: unable to configure the Docker daemon with file /etc/docker/daemon.json: invalid character '#' 
12月 29 20:28:10 xxx-pc systemd[1]: docker.service: Main process exited, code=exited, status=1/FAILURE
12月 29 20:28:10 xxx-pc systemd[1]: docker.service: Failed with result 'exit-code'.
12月 29 20:28:10 xxx-pc systemd[1]: Failed to start Docker Application Container Engine.|

Remove the # character in /etc/docker/daemon.json and the issue solved
