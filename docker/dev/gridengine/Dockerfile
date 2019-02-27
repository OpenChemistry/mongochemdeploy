FROM agaveapi/gridengine

RUN yum install -y yum-utils && \
  yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo && \
  yum install -y docker-ce-cli

RUN yum install -y centos-release-scl && \
  yum install -y python27 docker-io

COPY entrypoint.sh /entrypoint.sh

RUN ln -s /usr/bin/python2.6 /usr/local/bin/python

RUN yum update -y && \
  yum install -y singularity-runtime singularity

ENTRYPOINT [ "/entrypoint.sh" ]
CMD ["/usr/bin/supervisord"]
