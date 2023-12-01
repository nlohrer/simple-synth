FROM alpine

WORKDIR /src/cron
RUN mkdir /src/static
COPY ./cron .
RUN crontab delete-crontab

CMD ["crond", "-f"]