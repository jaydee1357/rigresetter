#!/bin/sh

mkdir /etc/rigresetter

wget https://raw.githubusercontent.com/jaydee1357/rigresetter/master/scripts/rig-resetter.py -O /etc/rigresetter/rig-resetter.py
wget https://raw.githubusercontent.com/jaydee1357/rigresetter/master/scripts/config.json -O /etc/rigresetter/config.json

# start cron
/usr/sbin/crond -f -l 8 && tail -f /var/log/cron/cron.log
