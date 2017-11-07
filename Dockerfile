FROM lsiobase/alpine.python:3.6

COPY scripts/crontab /tmp/crontab

RUN crontab /tmp/crontab \
    && rm -rf /tmpcrontab
