#!/bin/bash

set -xe

# install wget if it doesn' on system
#sudo apt-get update || true
#sudo apt-get install wget -y

# Download and place confd at /opt/confd
cd /tmp/
wget https://github.com/kelseyhightower/confd/releases/download/v0.16.0/confd-0.16.0-linux-amd64

sudo mkdir -p /opt/confd/bin
sudo mv confd-0.16.0-linux-amd64 /opt/confd/bin/confd

sudo chmod +x /opt/confd/bin/confd
sudo rm confd-0.16.0-linux-amd64* || true

# set path to bashrc
echo export PATH="\$PATH:/opt/confd/bin/" | sudo tee -a ~/.bashrc

# install schedule which is consumed to run task in regular interval
sudo pip install schedule

# Create al file for confd scheduler logging
sudo touch /var/log/confd.log

exit 0
