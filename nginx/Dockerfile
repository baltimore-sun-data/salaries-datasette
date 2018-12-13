FROM nginx

COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf

ARG APP_VERSION

RUN sed -i "s/VERSION_UNSET/$APP_VERSION/" /etc/nginx/conf.d/default.conf
