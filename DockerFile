FROM alpine:latest

RUN apk add --update python \
    && rm -rf /var/cache/apk/*

RUN touch crontab.tmp \
    && echo '*/10 * * * * python /etc/rigresetter/rig-monitor.py' > crontab.tmp \
    && crontab crontab.tmp \
    && rm -rf crontab.tmp

CMD ["/usr/sbin/crond", "-f", "-d", "0"]
