FROM conda/miniconda3:latest

RUN apt-get update && \
  apt-get install -y gcc && \
  rm -rf /var/lib/apt/lists/*

RUN conda update --all && \
  conda install psi4=1.2 psi4-rt=1.2 python=3.6 -c psi4

RUN pip install avogadro
RUN pip install click
RUN pip install jinja2

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /app

COPY src/* ./

ENTRYPOINT ["python", "main.py"]
