FROM lsiobase/alpine.python:3.6

RUN touch crontab.tmp \
    && mkdir /root/rigresetter \
    && echo '*/10 * * * * python /root/rigresetter/rig-resetter.py >> /root/rigresetter/rig-resetter.log' > crontab.tmp \
    && crontab crontab.tmp \
    && rm -rf crontab.tmp
    
COPY rig-resetter.py /root/rig-resetter.py
COPY config.json /root/config.json

RUN cp /root/rig-resetter.py /root/rigresetter/rig-resetter.py \
    && cp /root/config.json /root/rigresetter/config.json 

RUN ls -la /root/

RUN ls -la /root/rigresetter

CMD ["/usr/sbin/crond", "-f", "-d", "0"]
