

### Clean Disk

```shell
sudo du -h /var/cache/apt/archives
sudo apt-get autoclean
sudo apt-get clean
sudo apt-get autoremove

sudo apt-get install gtkorphan -y
# 開始菜單-》移除多餘的包
# or
sudo apt-get install deborphan -y

# unintall google cloud sdk
sudo apt-get autoremove --purge google-cloud-sdk

# 查看已安装的软件及其大小 -- Synaptic - 可在软件中心直接安装


```

