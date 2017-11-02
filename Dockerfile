FROM lsiobase/alpine.python:3.6

RUN touch crontab.tmp \
    && mkdir /root/rigresetter \
    && echo '*/10 * * * * python /root/rigresetter/rig-resetter.py >> /proc/1/fd/1 2>&1' > crontab.tmp \
    && crontab crontab.tmp \
    && rm -rf crontab.tmp

VOLUME /root/rigresetter

COPY rig-resetter.py /root/rig-resetter.py
COPY config.json /root/config.json

RUN cp /root/rig-resetter.py /root/rigresetter/rig-resetter.py \
    && cp /root/config.json /root/rigresetter/config.json 

RUN ls -la /root/rigresetter

RUN chmod +x /root/rigresetter/rig-resetter.py

CMD ["/usr/sbin/crond", "-f", "-d", "0"]
