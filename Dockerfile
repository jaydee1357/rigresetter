FROM lsiobase/alpine.python:3.6

RUN touch crontab.tmp \
    && mkdir /etc/rigresetter \
    && echo '*/10 * * * * python /etc/rigresetter/rig-resetter.py' > crontab.tmp \
    && crontab crontab.tmp \
    && rm -rf crontab.tmp

CMD ["/usr/sbin/crond", "-f", "-d", "0"]
