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

### Test result -- Success
~~~bash
XXX@XXX-pc:~$ sudo kubeadm config images pull
sudo kubeadm config images pulI1229 21:53:04.335565   18737 version.go:94] could not fetch a Kubernetes version from the internet: unable to get URL "https://dl.k8s.io/release/stable-1.txt": Get https://storage.googleapis.com/kubernetes-release/release/stable-1.txt: dial tcp [2404:6800:4008:c07::80]:443: connect: network is unreachable
I1229 21:53:04.335601   18737 version.go:95] falling back to the local client version: v1.13.1
[config/images] Pulled k8s.gcr.io/kube-apiserver:v1.13.1
[config/images] Pulled k8s.gcr.io/kube-controller-manager:v1.13.1
[config/images] Pulled k8s.gcr.io/kube-scheduler:v1.13.1
[config/images] Pulled k8s.gcr.io/kube-proxy:v1.13.1
[config/images] Pulled k8s.gcr.io/pause:3.1
[config/images] Pulled k8s.gcr.io/etcd:3.2.24
[config/images] Pulled k8s.gcr.io/coredns:1.2.6
~~~

### Reference
https://docs.docker.com/config/daemon/systemd/


### x509: certificate signed by unknown authority.
~~~
sudo docker run hello-world
Unable to find image 'hello-world:latest' locally
docker: Error response from daemon: Get https://registry-1.docker.io/v2/: x509: certificate signed by unknown authority.
See 'docker run --help'.
~~~

#### solution
```sh
sudo nano /lib/systemd/system/docker.service
```
Replace:
~~~
ExecStart=/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock
~~~
With: 
~~~
ExecStart=/usr/bin/dockerd --insecure-registry https://127.0.0.1:5000 -H fd:// --containerd=/run/containerd/containerd.sock
~~~

```sh
sudo systemctl daemon-reload
sudo systemctl restart docker
```
