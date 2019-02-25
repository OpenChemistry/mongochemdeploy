FROM agaveapi/gridengine

RUN yum install -y centos-release-scl && \
  yum install -y python27 docker-io

COPY entrypoint.sh /entrypoint.sh

COPY python27.sh /etc/profile.d/python27.sh


ENTRYPOINT [ "/entrypoint.sh" ]
CMD ["/usr/bin/supervisord"]
