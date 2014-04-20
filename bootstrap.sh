#!/bin/bash
alias dl="docker ps -l -q"
PROJECT_CODE=$1;

mkdir -p containers/$PROJECT_CODE
cp supervisord.conf containers/$PROJECT_CODE/
#docker build -t odhk.dev.code4.hk:0.1 - < Dockerfile_project

#TODO
#build base iamge if not exists
# docker build -t open-platform-hk/bootstrap:0.1 - < Dockerfile_base

#idealy shoudl genearte from host and inject to container, but docker insert don't support yet
#https://github.com/dotcloud/docker/issues/905

#create docker project
ssh-keygen -f ./containers/$PROJECT_CODE/id_rsa_$PROJECT_CODE -N ''
cd ./containers/$PROJECT_CODE
../../create_docker.py --code $PROJECT_CODE

chown -R ubuntu .

service nginx reload


##For Ops
##Distribute the key

##Ensure Amazon open 2222


##For Devs
#ssh -i /path/to/id_rsa root@demo.dev.code4.hk -p 2222

