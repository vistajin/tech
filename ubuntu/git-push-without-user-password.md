
~~~sh
$ git remote -v
origin	https://github.com/vistajin/tech.git (fetch)
origin	https://github.com/vistajin/tech.git (push)

$ git remote add origin git@github.com:vistajin/tech.git

in case: >>> fatal: 远程 origin 已经存在。run below and add again
$ git remote rm origin

$ ssh-keygen -t rsa -b 4096 -C "528189@qq.com"
$ eval "$(ssh-agent -s)"
$ ssh-add ~/.ssh/id_rsa
$ cat /home/vistajin/.ssh/id_rsa.pub
~~~

Paste the content to github in "Create new SSH key" page

~~~sh
$ git push --set-upstream origin master
~~~
