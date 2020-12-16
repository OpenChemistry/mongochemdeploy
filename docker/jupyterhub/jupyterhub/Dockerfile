FROM jupyterhub/jupyterhub:1.3

COPY requirements.txt /

RUN pip install -r /requirements.txt && \
    rm /requirements.txt

COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py

COPY wait-for-it.sh /
COPY entrypoint.sh /

ENTRYPOINT ["/entrypoint.sh"]
