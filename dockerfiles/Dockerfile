FROM ubuntu:20.04

ENV DEBIAN_FRONTEND="noninteractive" TZ="America/Seattle"

# For gcc
RUN apt-get update \
    && apt-get install -y build-essential

# For Java
RUN apt-get update \
    && apt-get install -y openjdk-14-jdk

RUN wget https://download.java.net/java/GA/jdk14.0.2/205943a0976c4ed48cb16f1043c5c647/12/GPL/openjdk-14.0.2_linux-x64_bin.tar.gz \
    tar xvf openjdk-14.0.2_linux-x64_bin.tar.gz -C /usr/lib/jvm \
    update-alternatives --install "/usr/bin/javac" "javac" "/usr/lib/jvm/jdk-14.0.2/bin/javac" 3 \
    update-alternatives --install "/usr/bin/java" "java" "/usr/lib/jvm/jdk-14.0.2/bin/java" 3 \
    update-alternatives --set "javac" "/usr/lib/jvm/jdk-14.0.2/bin/javac" \
    update-alternatives --set "java" "/usr/lib/jvm/jdk-14.0.2/bin/java"

# For Node
RUN apt-get update \
    && apt-get install -y curl \
    && curl -sL https://deb.nodesource.com/setup_14.x | bash \
    && apt-get install -y nodejs

# For Python
RUN apt-get update \
    && apt-get install -y python3.7
