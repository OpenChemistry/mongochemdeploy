FROM python:3.7

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt
RUN pip install torch_nightly -f https://download.pytorch.org/whl/nightly/cu100/torch_nightly.html
RUN pip install torchani

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY src/* /app/

ENTRYPOINT ["python", "/app/main.py"]
