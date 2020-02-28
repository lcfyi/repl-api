FROM openjdk:14-alpine

RUN echo /exit > exit.jsh
RUN echo >> exit.jsh

RUN jshell --help
