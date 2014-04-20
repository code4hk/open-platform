#!/bin/bash
alias dl="docker ps -l -q"
mkdir -p containers
##has to be generate in the host machine..

CODE=$1;


#docker build -t odhk.dev.code4.hk:0.1 - < Dockerfile_project

# docker build -t open-platform-hk/bootstrap:0.1 - < Dockerfile_base 
#create docker project
./create_docker.py --url $CODE".dev.code4.hk"

ssh-keygen -f ./containers/id_rsa_$CODE -N ''


docker build -t odhk.dev.code4.hk:0.1 .
# docker build -t odhk.dev.code4.hk:0.1 - < Dockerfile_base 

# ./create_docker.py --url $CODE".dev.code4.hk"


#after Docker Run

docker cp `dl`:/root/.ssh/id_rsa ./id_rsa_`dl`
chmod 600 ./id_rsa_`dl`/id_rsa
chown -R ubuntu ./id_rsa_`dl`

##For Ops
##Distribute the key

##Ensure Amazon open 2222


##For Devs
#ssh -i /path/to/id_rsa root@demo.dev.code4.hk -p 2222

#idealy shoudl genearte from host and inject to container, but docker insert don't support yet
#https://github.com/dotcloud/docker/issues/905

#quick hack


RUN cat ./containers/id_rsa_`dl`.pub >> /root/.ssh/authorized_keys
RUN chmod 600 ~/.ssh/authorized_keys

