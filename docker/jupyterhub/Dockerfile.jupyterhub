FROM jupyterhub/jupyterhub:0.9.4

# Install dockerspawner, postgres
RUN /opt/conda/bin/conda install psycopg2=2.7 && \
    /opt/conda/bin/conda clean -tipsy && \
    /opt/conda/bin/pip install \
    dockerspawner==0.10.0

RUN  /opt/conda/bin/pip install girder-jupyterhub

COPY jupyterhub_config.py  /srv/jupyterhub/jupyterhub_config.py

#COPY login.html /opt/conda/share/jupyter/hub/templates
