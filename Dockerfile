FROM ubuntu
MAINTAINER lauchunyin@gmail.com
RUN echo "deb http://archive.ubuntu.com/ubuntu precise universe" >> /etc/apt/sources.list
RUN echo "We are creating the image.."
RUN apt-get update
RUN apt-get -y install python3 git vim openssh-server
#RUN sed -i -e "s/PermitRootLogin\syes/PermitRootLogin no/g" /etc/ssh/sshd_config

RUN mkdir /var/run/sshd 

RUN ssh-keygen -f /root/.ssh/id_rsa -N ''
RUN  echo "    IdentityFile /root/.ssh/id_rsa" >> /etc/ssh/ssh_config
EXPOSE 80
EXPOSE 22


CMD    /usr/sbin/sshd -D

