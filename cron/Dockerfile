FROM alpine

WORKDIR /src/cron
RUN mkdir /src/static
COPY ./cron .
RUN apk add tini
RUN crontab delete-crontab

ENTRYPOINT ["tini", "--", "/usr/sbin/crond", "-f"]