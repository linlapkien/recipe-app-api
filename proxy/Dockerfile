FROM nginxinc/nginx-unprivileged:1-alpine
LABEL maintainer="linlapkien.com"

# copy default.conf.tpl nginx configuration file to docker image store at /etc/nginx/default.conf.tpl
COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
COPY ./uwsgi_params /etc/nginx/uwsgi_params
COPY ./run.sh /run.sh

ENV LISTEN_PORT=8000
ENV APP_HOST=app
ENV APP_PORT=9000

# First change root user to nginx user
USER root

# create directory for static files
RUN mkdir -p /vol/static && \
    chmod 755 /vol/static && \
    touch /etc/nginx/conf.d/default.conf && \
    # change owner of default.conf file to nginx user
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    chmod +x /run.sh

# create volume for static files
VOLUME /vol/static

# Then change user to nginx user when run docker image
USER nginx

CMD ["/run.sh"]
