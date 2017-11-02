FROM lsiobase/alpine.python:3.6

RUN touch crontab.tmp \
    && mkdir /etc/rigresetter \
    && echo '*/10 * * * * python /etc/rigresetter/rig-resetter.py >> /proc/1/fd/1 2>&1' > crontab.tmp \
    && crontab crontab.tmp \
    && rm -rf crontab.tmp

ADD rig-resetter.py /etc/rigresetter/rig-resetter.py
ADD config.json /etc/rigresetter/config.json

RUN chmod +x /etc/rigresetter/rig-resetter.py

VOLUME /etc/rigresetter

CMD ["/usr/sbin/crond", "-f", "-d", "0"]
