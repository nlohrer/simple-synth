FROM nginx:latest
COPY ./web /data/web
RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf
