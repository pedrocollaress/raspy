# Raspy IOT

### Make the Remote Connection

- **Host**: `10.10.40.1`
- **Password**: `sistemas`

### System Update

Use the following commands to update the system.

```bash
apt update
apt full-upgrade

apt install git-core
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
python setup.py install

sed -i 's/^CONF_SWAPSIZE=.*/CONF_SWAPSIZE=1024/' /etc/dphys-swapfile
dphys-swapfile setup
dphys-swapfile swapon
```
