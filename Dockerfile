FROM lsiobase/alpine.python:3.6

RUN touch crontab.tmp \
    && mkdir /root/rigresetter \
    && echo '*/10 * * * * python /root/rigresetter/rig-resetter.py >> /proc/1/fd/1 2>&1' > crontab.tmp \
    && crontab crontab.tmp \
    && rm -rf crontab.tmp

COPY rig-resetter.py /root/rigresetter/rig-resetter.py
COPY config.json /root/rigresetter/config.json

RUN chmod +x /root/rigresetter/rig-resetter.py

VOLUME /root/rigresetter

CMD ["/usr/sbin/crond", "-f", "-d", "0"]
