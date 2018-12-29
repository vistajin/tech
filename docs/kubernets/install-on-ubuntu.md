
~~~sh
sudo proxychains4 apt-get update && sudo proxychains4 apt-get install -y apt-transport-https

sudo proxychains4 curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

# su to root
cat <<EOF > /etc/apt/sources.list.d/kubernetes.list
> deb http://apt.kubernetes.io/ kubernetes-xenial main
> EOF

exit

sudo proxychains4 apt-get update

sudo proxychains4 apt-get install -y kubelet kubeadm kubectl

~~~
