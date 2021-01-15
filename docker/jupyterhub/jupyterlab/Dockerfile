FROM jupyterhub/singleuser

USER root

RUN apt-get update && apt-get -y install git

USER jovyan

# Fix python to 3.7, the latest supported by the avogadro wheel
RUN /opt/conda/bin/conda install python=3.7

RUN /opt/conda/bin/pip install jupyterhub==1.3.0

RUN /opt/conda/bin/pip install jupyterlab==3.0.4

RUN  /opt/conda/bin/pip install girder-jupyterhub

RUN  /opt/conda/bin/pip install girder-jupyter

RUN /opt/conda/bin/pip install matplotlib

RUN git clone https://github.com/OpenChemistry/openchemistrypy.git openchemistrypy && \
  /opt/conda/bin/pip install -e openchemistrypy

RUN git clone https://github.com/OpenChemistry/jupyterlab_cjson.git && \
  cd jupyterlab_cjson && \
  npm install && \
  npm run build && \
  jupyter labextension link .
