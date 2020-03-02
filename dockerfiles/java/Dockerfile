FROM {}

RUN jshell -h

COPY code /code.jsh
COPY exit.jsh /exit.jsh

CMD ["jshell", "code.jsh", "exit.jsh"]
