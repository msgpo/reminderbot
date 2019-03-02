#!/bin/sh
# scp reminderbot.tgz root@wherever:/root/
# ssh root@wherever 'bash -s' < bootstrap.sh

#TODO Create non-root user

ufw allow 22
ufw enable

# Create user
adduser --system --no-create-home reminderbot
addgroup wheel
usermod -a -G wheel reminderbot

# Unpackage
install_target=/opt/reminderbot
mkdir -p $install_target
cd /root
tar xzf reminderbot.tgz -C $install_target

# Python setup
DEBIAN_FRONTEND=noninteractive apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y python3-pip
python3 -m venv /opt/venvs/reminderbot
/opt/venvs/reminderbot/bin/pip install wheel
/opt/venvs/reminderbot/bin/pip install --requirement /opt/reminderbot/requirements.txt

# Handle permissions now that everything is installed correctly
chown --recursive reminderbot:wheel "$install_target"

# Set cron job
crontab -u reminderbot "$install_target/crontab.txt"
