FROM php:7.1-fpm

ARG project

RUN apt-get update && \
    apt install -y libxml2-dev && \
    apt install -y libxslt-dev && \
    docker-php-ext-install xsl && \
    docker-php-ext-install xml