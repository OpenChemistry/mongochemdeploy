FROM continuumio/miniconda3:latest

RUN conda install python=3.6
RUN conda install -c conda-forge rdkit
RUN conda install -c openbabel openbabel
RUN conda install -c anaconda tensorflow

RUN pip install avogadro

RUN git clone https://github.com/hachmannlab/chemml.git
RUN pip install -e ./chemml

# For now copy model files to the hardcoded expected location
RUN mkdir -p ./chemml/chemml/datasets/data/models/keras/organic_lorentz_lorenz/
COPY x_standard_scaler.csv chemml/chemml/datasets/data/models/keras/organic_lorentz_lorenz/
COPY y_standard_scaler.csv chemml/chemml/datasets/data/models/keras/organic_lorentz_lorenz/
COPY Morgan_100k.h5 chemml/chemml/datasets/data/models/keras/organic_lorentz_lorenz/

COPY src/* /app/

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt


ENTRYPOINT ["python", "/app/main.py"]
