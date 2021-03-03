FROM python:3.7
#FROM continuumio/miniconda3:4.8.2 as build

# Switch back to root, set up the environment.
#USER 0
#ENV PATH /opt/conda/bin/:$PATH

COPY src/* /app/
COPY requirements.txt /app/

# Update apt, install blas/lapack for psi4, then Python deps, and then build.
RUN apt-get update && \
  apt-get install -y libblas-dev liblapack-dev && \
  cd /root && \
  # Needed for projectq
  pip install pybind11 && \
  pip install -r /app/requirements.txt && \
  wget https://github.com/psi4/psi4/archive/v1.3.2.tar.gz && \
  tar zxvf v1.3.2.tar.gz && \
  mkdir build && \
  cd build && \
  cmake ../psi4-1.3.2 && make -j10 install && \
  rm -rf /usr/local/psi4/share/psi4/samples && \
  cd / && rm -rf /root && mkdir /root && \
  rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH /usr/local/psi4/lib:$PYTHONPATH
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

ENTRYPOINT ["python", "/app/main.py"]
