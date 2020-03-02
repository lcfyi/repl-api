COPY code /code.cpp

RUN gcc -o app code.cpp

CMD ["./app"]
