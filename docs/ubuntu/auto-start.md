1. Create rc-local.service: 
```bash
sudo nano /etc/systemd/system/rc-local.service
```
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
<pre><code>sudo nano /etc/rc.local</code></pre>

3. Add shell script that want to run when start up:
<pre><bash>
sudo sslocal -c /etc/shadowsocks.json
</bash></pre>

And then run below command:
<pre><code>
ln -s /lib/systemd/system/rc.local.service /etc/systemd/system/ 
</code></pre>
