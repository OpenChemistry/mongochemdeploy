#!/bin/bash

# Setup docker group
DOCKER_SOCKET=/var/run/docker.sock
DOCKER_GROUP=docker

if [ -S ${DOCKER_SOCKET} ]; then
    DOCKER_GID=$(stat -c '%g' ${DOCKER_SOCKET})
    groupadd -for -g ${DOCKER_GID} ${DOCKER_GROUP}
    usermod -aG ${DOCKER_GROUP} testuser
fi

chmod a+w /data

# From docker_entrypoint.sh
set -e

source /usr/share/gridengine/default/common/settings.sh

echo "$HOSTNAME" >  /usr/share/gridengine/default/common/act_qmaster
echo "domain $HOSTNAME" >> /etc/resolv.conf
/etc/init.d/sgemaster start
qconf -mattr "queue" "hostlist" "$HOSTNAME" "debug"
qconf -as $HOSTNAME

# Set the number of slots. We will use half the number of processors.
numProcsToUse=$(( $(nproc --all) / 2))
qconf -rattr queue slots $numProcsToUse debug

# Run whatever the user wants to
exec "$@"
