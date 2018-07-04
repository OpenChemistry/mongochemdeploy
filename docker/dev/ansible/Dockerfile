FROM python:3.5-slim

RUN apt-get update && apt-get -y install \
  git

RUN pip install ansible && \
  pip install girder_client

WORKDIR /ansible

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
