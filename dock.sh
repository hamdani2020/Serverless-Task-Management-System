#!/bin/bash

DOCKER_IMAGE_NAME="react-app:latest"
DOCKER_REPO_NAME=lusitech/react-app:latest
DOCKER_FILE_PATH="."
echo "building the docker image"
docker build -t $DOCKER_IMAGE_NAME $DOCKER_FILE_PATH
echo "Tagging the image react-app:latest"
docker tag $DOCKER_IMAGE_NAME $DOCKER_REPO_NAME
docker push $DOCKER_REPO_NAME
