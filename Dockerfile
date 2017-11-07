FROM lsiobase/alpine.python:3.6

RUN apk update && apk upgrade && \
    apk add --no-cache bash git openssh

