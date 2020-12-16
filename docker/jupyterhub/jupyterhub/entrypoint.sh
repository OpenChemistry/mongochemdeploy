#!/usr/bin/env bash

/wait-for-it.sh -t 30 hub-db:5432 -- jupyterhub --debug -f /srv/jupyterhub/jupyterhub_config.py
