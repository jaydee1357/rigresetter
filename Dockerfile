FROM lsiobase/alpine.python:3.6

RUN touch crontab.tmp \
    && mkdir /etc/rigresetter \
    && echo '*/10 * * * * python /etc/rigresetter/rig-resetter.py > /dev/pts/1' > crontab.tmp \
    && crontab crontab.tmp \
    && rm -rf crontab.tmp

ADD rig-resetter.py /etc/rigresetter/rig-resetter.py

CMD ["/usr/sbin/crond", "-f", "-d", "0"]
