### Unable to reach k8s.gcr.io
~~~sh
XXX@XXX-pc:~$ sudo kubeadm config images pull
I1229 21:30:09.472929   12687 version.go:94] could not fetch a Kubernetes version from the internet: unable to get URL "https://dl.k8s.io/release/stable-1.txt": Get https://storage.googleapis.com/kubernetes-release/release/stable-1.txt: dial tcp [2404:6800:4008:c07::80]:443: connect: network is unreachable
I1229 21:30:09.472961   12687 version.go:95] falling back to the local client version: v1.13.1
failed to pull image "k8s.gcr.io/kube-apiserver:v1.13.1": output: Error response from daemon: Get https://k8s.gcr.io/v2/: dial tcp [2404:6800:4008:c00::52]:443: connect: network is unreachable
, error: exit status 1
~~~

### Try to solve by adding proxy to docker
~~~sh
sudo nano /etc/systemd/system/docker.service.d/http-proxy.conf
~~~


~~~bash
[Service]
#Environment="HTTP_PROXY=http://127.0.0.1:8119/"
#Environment="HTTPS_PROXY=http://127.0.0.1:8119/"
Environment="HTTP_PROXY=socks5://127.0.0.1:1080"
Environment="HTTPS_PROXY=socks5://127.0.0.1:1080"
~~~

~~~bash
sudo systemctl daemon-reload
sudo systemctl restart docker.service

sudo kubeadm config images pull
~~~
