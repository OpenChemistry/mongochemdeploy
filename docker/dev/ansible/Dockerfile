FROM python:3.5-slim

RUN apt-get update && apt-get -y install \
  git \
  sshpass


RUN pip install ansible && \
  pip install girder_client

WORKDIR /ansible

COPY ansible/entrypoint.sh /entrypoint.sh
COPY wait-for-it.sh /wait-for-it.sh


ENTRYPOINT ["/wait-for-it.sh", "-t", "30", "girder:8080",  "--", "/entrypoint.sh"]
