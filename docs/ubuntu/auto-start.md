1. Create rc-local.service: 
~~~bash
sudo nano /etc/systemd/system/rc-local.service
~~~
<pre><code>[Unit]
Description=/etc/rc.local Compatibility
ConditionPathExists=/etc/rc.local

[Service]
Type=forking
ExecStart=/etc/rc.local start
TimeoutSec=0
StandardOutput=tty
RemainAfterExit=yes
SysVStartPriority=99

[Install]
WantedBy=multi-user.target
</code></pre>

2. There is no /etc/rc.local in 18.04, need to create it manually:
```sh
sudo nano /etc/rc.local
```
<pre><code>
#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

sslocal -c /etc/shadowsocks.json

exit 0
</code></pre>

3. And then run below command:
~~~sh
sudo chmod +x /etc/rc.local
sudo systemctl enable rc-local
~~~
