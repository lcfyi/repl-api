FROM python:3.8.2-alpine

RUN rm -f /sbin/apk \
     rm -rf /etc/apk \
     rm -rf /lib/apk \
     rm -rf /usr/share/apk \
     rm -rf /var/lib/apk

RUN pip install requests
