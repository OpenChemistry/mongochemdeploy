FROM jupyterhub/singleuser

USER root

RUN apt-get update && apt-get -y install git

USER jovyan

RUN /opt/conda/bin/pip install jupyterhub==0.9.4

RUN /opt/conda/bin/pip install jupyterlab==0.35.2

RUN  /opt/conda/bin/pip install girder-jupyterhub

RUN  /opt/conda/bin/pip install girder-jupyter

RUN  git clone https://github.com/OpenChemistry/openchemistrypy.git openchemistrypy && \
  /opt/conda/bin/pip install -e openchemistrypy

RUN git clone https://github.com/OpenChemistry/jupyterlab_cjson.git && \
  cd jupyterlab_cjson && \
  /opt/conda/bin/pip install -e . && \
  cd labextension && \
  npm install && \
  npm run build && \
  jupyter labextension link .
