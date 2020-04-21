FROM continuumio/miniconda3:4.8.2-alpine as build

# Switch back to root, set up the environment.
USER 0
ENV PATH /opt/conda/bin/:$PATH

# Create a fresh environment for the Psi4 package.
RUN conda install -c conda-forge conda-pack
COPY --chown=anaconda:anaconda environment.yml /app/
RUN conda env create -f /app/environment.yml
# Package the environment, ready to be moved.
RUN conda pack -n psi4 -o /app/psi4.tar.gz
RUN mkdir /psi4
RUN tar -xzf /app/psi4.tar.gz -C /psi4
RUN apk add --no-cache bash git
SHELL ["/bin/bash", "--login", "-c"]
# Clean up for the prefix it will be used in, remove files we don't need.
RUN source /psi4/bin/activate && \
  conda-unpack && \
  find /psi4/ -follow -type f -name '*.a' -delete && \
  find /psi4/ -follow -type f -name '*.js.map' -delete && \
  conda clean -afy
RUN rm /app/psi4.tar.gz /app/environment.yml

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Multi-stage build to reduce image size
FROM continuumio/miniconda3:4.8.2-alpine

COPY --from=build /psi4/. /psi4/
COPY --chown=anaconda:anaconda src/* /app/

USER 0
ENV PATH /psi4/bin:$PATH

ENTRYPOINT ["/psi4/bin/python3", "/app/main.py"]
