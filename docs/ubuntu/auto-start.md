Note:
There is no /etc/rc.local in 18.04, need to create it manually:
<pre><code>sudo touch /etc/rc.local</code></pre>

Add shell script that want to run when start up:
<pre><code>
sudo sslocal -c /etc/shadowsocks.json
</code></pre>

And then run below command:
<pre><code>
ln -s /lib/systemd/system/rc.local.service /etc/systemd/system/ 
</code></pre>
