
~~~sh
$ git remote -v
origin	https://github.com/vistajin/dataflow-training.git (fetch)
origin	https://github.com/vistajin/dataflow-training.git (push)

$ git remote add origin git@github.com:vistajin/dataflow-training.git
$ ssh-keygen -t rsa -b 4096 -C "528189@qq.com"
$ eval "$(ssh-agent -s)"
$ ssh-add ~/.ssh/id_rsa
$ cat /home/vistajin/.ssh/id_rsa.pub
~~~

Paste the content to github in "Create new SSH key" page

~~~sh
$ git push --set-upstream origin master
~~~
