
~~~sh
$ git remote -v
origin	https://github.com/vistajin/tech.git (fetch)
origin	https://github.com/vistajin/tech.git (push)

# this is to swith remote URLs from HTTPS to SSH
# reference: https://help.github.com/en/github/using-git/changing-a-remotes-url#switching-remote-urls-from-https-to-ssh
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

### Sometimes using ssh won't work and got below error:
~~~
ERROR: Unexpected http response: ''.
FATAL: failed to begin relaying via HTTP.
fatal: 无法读取远程仓库。

请确认您有正确的访问权限并且仓库存在。
~~~

Use below:
```
git remote rm origin
git remote add origin https://vistajin:<password>@github.com/vistajin/tech.git
git branch --set-upstream-to=origin/master master
```

