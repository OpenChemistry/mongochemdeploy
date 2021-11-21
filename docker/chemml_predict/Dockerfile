FROM continuumio/miniconda3:latest

RUN conda install python=3.8
RUN conda install -c conda-forge openbabel rdkit nb_conda_kernels python-graphviz
RUN pip install chemml

COPY src/* /app/

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt


ENTRYPOINT ["python", "/app/main.py"]
