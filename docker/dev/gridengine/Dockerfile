FROM agaveapi/gridengine

RUN yum install -y yum-utils && \
  yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo && \
  yum install -y docker-ce-cli

RUN yum install -y centos-release-scl && \
  yum install -y python27 docker-io

COPY entrypoint.sh /entrypoint.sh

ENV LD_LIBRARY_PATH /opt/rh/python27/root/usr/lib64

RUN ln -fs /opt/rh/python27/root/usr/bin/python /usr/bin/python && \
  ln -s /usr/bin/python /usr/local/bin/python

ENTRYPOINT [ "/entrypoint.sh" ]
CMD ["/usr/bin/supervisord"]
