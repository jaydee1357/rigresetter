FROM lsiobase/alpine.python:3.6

COPY scripts/crontab /tmp/crontab \
     && scripts/start.sh /start.sh

RUN crontab /tmp/crontab \
    && rm -rf /tmpcrontab

CMD ["/start.sh"]
