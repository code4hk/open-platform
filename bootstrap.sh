#!/bin/bash
alias dl="docker ps -l -q"
mkdir -p containers

PROJECT_CODE=$1;
#docker build -t odhk.dev.code4.hk:0.1 - < Dockerfile_project

#TODO
#build base iamge if not exists
# docker build -t open-platform-hk/bootstrap:0.1 - < Dockerfile_base 

#idealy shoudl genearte from host and inject to container, but docker insert don't support yet
#https://github.com/dotcloud/docker/issues/905

#create docker project
ssh-keygen -f ./containers/id_rsa_$PROJECT_CODE -N ''
cd ./containers
../create_docker.py --code $PROJECT_CODE


##For Ops
##Distribute the key

##Ensure Amazon open 2222


##For Devs
#ssh -i /path/to/id_rsa root@demo.dev.code4.hk -p 2222

