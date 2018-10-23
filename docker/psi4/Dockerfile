FROM conda/miniconda3:latest

RUN apt-get update && \
  apt-get install -y gcc && \
  rm -rf /var/lib/apt/lists/*

RUN conda update --all && \
  conda install psi4=1.2 psi4-rt=1.2 python=3.6 -c psi4

ENTRYPOINT ["/usr/local/bin/psi4"]

