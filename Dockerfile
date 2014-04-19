FROM ubuntu
MAINTAINER lauchunyin@gmail.com
RUN echo "deb http://archive.ubuntu.com/ubuntu precise universe" >> /etc/apt/sources.list
RUN echo "We are creating the image.."
RUN apt-get update
RUN apt-get -y install python3 git vim openssh-server
#RUN sed -i -e "s/PermitRootLogin\syes/PermitRootLogin no/g" /etc/ssh/sshd_config


##lazily generate the key in container itself..
RUN ssh-keygen -f /root/.ssh/id_rsa -N ‘'

RUN cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys
RUN chmod 600 ~/.ssh/authorized_keys

RUN mkdir /var/run/sshd 

EXPOSE 80
EXPOSE 22

CMD    /usr/sbin/sshd -D


