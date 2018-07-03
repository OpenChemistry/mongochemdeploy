#!/bin/bash
SCRIPT=$(readlink -f "$0")
SCRIPT_DIR=$(dirname "$SCRIPT")
REPO_DIR="$SCRIPT_DIR/.."

export JUPYTERHUB_DOCKER_DIR=$REPO_DIR/docker/jupyterhub
export DEV_DOCKER_DIR=$REPO_DIR/docker/dev
export GIRDER_DOCKER_DIR=$REPO_DIR/docker/girder


pushd .
cd $REPO_DIR/docker
docker-compose -f docker-compose.yml -f girder/docker-compose.yml -f jupyterhub/docker-compose.yml up
popd
