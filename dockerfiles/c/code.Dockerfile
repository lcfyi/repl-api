COPY code /code.c

RUN gcc -o app code.c

CMD ["./app"]
