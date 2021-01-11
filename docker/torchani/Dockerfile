FROM python:3.7

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt
RUN pip install torch==1.4.0
RUN pip install torchani==1.2

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY src/* /app/

ENTRYPOINT ["python", "/app/main.py"]
