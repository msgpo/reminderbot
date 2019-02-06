#!/bin/sh
# scp reminderbot.tgz root@wherever:/root/
# ssh root@wherever 'bash -s' < bootstrap.sh

# Create user
adduser --system reminderbot
addgroup wheel
usermod -a -G wheel reminderbot

# Unpackage
install_target=/opt/reminderbot
mkdir -p $install_target
cd /root
tar xzf reminderbot.tgz -C $install_target

# Python setup
DEBIAN_FRONTEND=noninteractive apt-get update
#apt-get install -y python3-pip python3-venv
DEBIAN_FRONTEND=noninteractive apt-get install -y python3-pip
pip3 install pipenv

# Python dependencies
cd $install_target
pipenv sync

# Handle permissions now that everything is installed correctly
chown --recursive reminderbot:wheel "$install_target"

# Set cron job
crontab "$install_target/crontab.txt"
