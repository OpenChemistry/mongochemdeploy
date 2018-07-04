#!/bin/bash
SCRIPT=$(readlink -f "$0")
SCRIPT_DIR=$(dirname "$SCRIPT")
REPO_DIR="$SCRIPT_DIR/.."

export JUPYTERHUB_DOCKER_DIR=$REPO_DIR/docker/jupyterhub
export DEV_DOCKER_DIR=$REPO_DIR/docker/dev
export GIRDER_DOCKER_DIR=$REPO_DIR/docker/girder

pushd .
cd $REPO_DIR/docker/dev

FILES="docker-compose.yml ../girder/docker-compose.yml ../jupyterhub/docker-compose.yml"


#CMD='docker-compose -f docker-compose.yml -f ../girder/docker-compose.yml -f ../jupyterhub/docker-compose.yml -f docker-compose.client.yml up

FILE="dev.env"
while IFS== read -r name value 
do
        case "$name" in \#*) continue ;; esac
        FILES="$FILES  docker-compose.${name,,}.yml"
done <"$FILE"

CMD='docker-compose'

for f in $FILES; do
    CMD="$CMD -f $f" 
done

CMD="$CMD up"
$CMD

popd
