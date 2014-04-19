FROM ubuntu
MAINTAINER lauchunyin@gmail.com
RUN echo "We are creating the image.."
RUN apt-get update
RUN apt-get -y install python3 git vim openssh-server
RUN sed -i -e "s/PermitRootLogin\syes/PermitRootLogin no/g" /etc/ssh/sshd_config

EXPOSE 80
EXPOSE 22

