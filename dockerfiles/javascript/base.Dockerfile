FROM node:13.8.0-alpine

RUN rm -f /sbin/apk \
     rm -rf /etc/apk \
     rm -rf /lib/apk \
     rm -rf /usr/share/apk \
     rm -rf /var/lib/apk
