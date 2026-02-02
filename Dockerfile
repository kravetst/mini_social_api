FROM ubuntu:latest
LABEL authors="Bodja"

ENTRYPOINT ["top", "-b"]