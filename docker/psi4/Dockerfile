FROM conda/miniconda3:latest

RUN apt-get update && \
  apt-get install -y gcc git && \
  rm -rf /var/lib/apt/lists/*

RUN conda update --all && \
  conda install psi4=1.2 psi4-rt=1.2 python=3.6 -c psi4

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY src/* /app/

ENTRYPOINT ["python", "/app/main.py"]
