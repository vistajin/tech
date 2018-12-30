
### 6443 was refused - did you specify the right host or port?
~~~sh
xxx@xxx-pc:~$ kubectl get pods
The connection to the server 192.168.31.24:6443 was refused - did you specify the right host or port?
~~~

#### Solution
~~~sh
export KUBECONFIG=$HOME/admin.conf
~~~
