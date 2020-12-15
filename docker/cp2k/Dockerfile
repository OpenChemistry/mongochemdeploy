FROM ubuntu:18.04

# Install ssh, which is a runtime dep of the ubuntu cp2k package
# (due to its usage of MPI)
RUN apt-get update && \
  apt-get install -y \
    ssh \
    git \
    cp2k \
    python3 \
    python3-pip && \
  rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip3 install -r /app/requirements.txt

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY src/* /app/

ENTRYPOINT ["python3", "/app/main.py"]
