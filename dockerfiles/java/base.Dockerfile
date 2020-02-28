FROM openjdk:14-alpine

RUN rm -f /sbin/apk \
     rm -rf /etc/apk \
     rm -rf /lib/apk \
     rm -rf /usr/share/apk \
     rm -rf /var/lib/apk

RUN echo -e "/exit\n" > exit.jsh

RUN jshell --help
