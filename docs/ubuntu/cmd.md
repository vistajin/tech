### Firewall related
```sh
sudo ufw status
sudo ufw allow 8080
sudo ufw delete allow 8080
sudo ufw allow from 192.168.1.1
sudo ufw enable
sudo ufw default deny  # not allow any access by default
默认的 incoming 策略更改为 “deny”
（请相应地更新你的防火墙规则）
```
### Bridge related
```sh
ip addr
sudo brctl show
```
