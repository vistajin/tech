https://vitux.com/how-to-install-notepad-on-ubuntu/

```shell
sudo apt list
sudo apt-get install snapd snapd-xdg-open
sudo snap install notepad-plus-plus
sudo snap connect notepad-plus-plus:process-control
sudo snap connect notepad-plus-plus:removable-media
sudo snap connect notepad-plus-plus:hardware-observe
sudo snap connect notepad-plus-plus:cups-control
# MUST restart to take effect
```

