FROM        ubuntu:19.04

LABEL maintainer="Muammar El khatib <melkhatibr@lbl.gov>"

ENV         LC_ALL=C.UTF-8
ENV         LANG=C.UTF-8
ARG         tarball
ENV         ORCA_TARBALL=$tarball

RUN         apt-get update \
            && apt-get -y upgrade && apt-get -y install xz-utils python3 \
            && apt-get -y install python3-pip openbabel libopenbabel-dev \
            && apt-get -y install swig pkg-config\
            && apt-get autoclean && apt-get autoremove

WORKDIR     /opt

# Adding ORCA... A 3GB tarball...
COPY        $ORCA_TARBALL /opt/

RUN         mkdir orca && tar Jxvf $ORCA_TARBALL -C /opt/orca --strip-components 1 \
            && rm $ORCA_TARBALL

ENV         PATH=/opt/orca:$PATH

WORKDIR     /app/
COPY        requirements.txt /app/
RUN         pip3 install -r /app/requirements.txt

COPY        src/* /app/

WORKDIR     /data

ENTRYPOINT ["python3", "/app/main.py"]
