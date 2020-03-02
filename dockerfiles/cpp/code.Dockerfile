COPY code /code.cpp

RUN g++ -o app code.cpp

CMD ["./app"]
