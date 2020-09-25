#!/bin/bash
# Add swap space
sudo fallocate -l 1G /swapfile
sudo dd if=/dev/zero of=/swapfile bs=1024 count=1048576
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile swap swap defaults 0 0' | sudo tee -a /etc/fstab

# Install eos-related packages
sudo wget https://github.com/eosio/eos/releases/download/v1.8.6/eosio_1.8.6-1-ubuntu-18.04_amd64.deb
sudo apt install ./eosio_1.8.6-1-ubuntu-18.04_amd64.deb
sudo wget https://github.com/eosio/eosio.cdt/releases/download/v1.6.3/eosio.cdt_1.6.3-1-ubuntu-18.04_amd64.deb
sudo apt install ./eosio.cdt_1.6.3-1-ubuntu-18.04_amd64.deb

# Update python 
sudo apt install python3-pip
pip3 install toml
pip3 install numpy

# Load built contracts