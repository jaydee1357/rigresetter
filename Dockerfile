FROM lsiobase/alpine.python:3.6

COPY scripts/crontab crontab.tmp \
     && scripts/start.sh /start.sh

RUN crontab crontab.tmp \
    && rm -rf crontab.tmp

CMD ["/start.sh"]
