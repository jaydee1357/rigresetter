FROM alpine-python3

RUN touch crontab.tmp \
    && mkdir /etc/rigresetter \
    && cp rig-resetter.py /etc/rigresetter/rig-resetter.py \
    && echo '*/10 * * * * python /etc/rigresetter/rig-resetter.py' > crontab.tmp \
    && crontab crontab.tmp \
    && rm -rf crontab.tmp

CMD ["/usr/sbin/crond", "-f", "-d", "0"]
