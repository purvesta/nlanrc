FROM ubuntu:latest

MAINTAINER Tanner Purves <tanner@neverlanctf.org>

#EXPOSE 1099
#EXPOSE 5005

RUN mkdir /nlanrc
COPY . /nlanrc
WORKDIR /nlanrc

ENTRYPOINT ["python","nlanrc.py"]
