#!/bin/sh
ansible-galaxy install -r requirements.yml
ansible-playbook -M /root/.ansible/roles/girder.girder/library -i inventory/localhost dev.yml
