FROM ubuntu:20.04

ENV DEBIAN_FRONTEND="noninteractive" TZ="America/Seattle"

# For gcc
RUN apt-get update \
    && apt-get install -y build-essential

# For Java
RUN apt-get update \
    && apt-get install -y openjdk-14-jdk

# For Node
RUN apt-get update \
    && apt-get install -y curl \
    && curl -sL https://deb.nodesource.com/setup_14.x | bash \
    && apt-get install -y nodejs

# For Python
RUN apt-get update \
    && apt-get install -y python3.7
