FROM python:3.6

RUN adduser --system celery

# Install cumulus
RUN git clone https://github.com/Kitware/cumulus.git /cumulus && \
  pip install --no-cache-dir -r /cumulus/requirements.txt && \
  pip install --no-cache-dir -e /cumulus && \
  pip install --no-cache-dir girder

# Set the broker URL
RUN sed -i s/localhost/rabbitmq/g /cumulus/cumulus/celery/commonconfig.py

RUN mkdir /keys && chown -R celery  /keys

COPY config.json /cumulus/cumulus/conf/config.json

RUN chown -R celery  /cumulus

# Install Avogadro
RUN pip install avogadro

# Install openchemistry
RUN git clone https://github.com/OpenChemistry/openchemistrypy.git /openchemistrypy && \
  chown -R celery  /openchemistrypy

USER celery
