FROM lsiobase/alpine.python:3.6

COPY scripts/start.sh /start.sh

CMD ["/start.sh"]
