#!/bin/sh

mkdir /etc/rigresetter

wget https://raw.githubusercontent.com/jaydee1357/rigresetter/master/scripts/rig-resetter.py -O /etc/rigresetter/rig-resetter.py

# start cron
/usr/sbin/crond -f -l 8
