https://github.com/rofl0r/proxychains-ng

~~~sh
git clone https://github.com/rofl0r/proxychains-ng.git
cd proxychains-ng
./configure --prefix=/usr --sysconfdir=/etc
make
sudo make install
sudo make install-config
sudo nano /etc/proxychains.conf
~~~

~~~bash
[ProxyList]
# add proxy here ...
# meanwile
# defaults set to "tor"
socks5  127.0.0.1 1080
~~~

### Usage:
sudo proxychains4 apt-get update

-----------------------------------------------------------
Another method that don't need to use proxychains4
~~~sh
sudo apt-get install polipo
nano /etc/polipo/config
~~~

~~~bash
logSyslog = true
logFile = /var/log/polipo/polipo.log

proxyAddress = "0.0.0.0"

socksParentProxy = "127.0.0.1:1080"
socksProxyType = socks5

chunkHighMark = 50331648
objectHighMark = 16384

serverMaxSlots = 64
serverSlots = 16
serverSlots1 = 32
~~~

~~~sh
sudo /etc/init.d/polipo restart
export http_proxy="http://127.0.0.1:8123/"
export https_proxy="https://127.0.0.1:8123/"
~~~
### Node: port is 8123, not 1080!
