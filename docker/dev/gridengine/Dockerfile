FROM agaveapi/gridengine

RUN yum install -y docker-io \
  python

COPY docker_group.sh /docker_group.sh

RUN ln -s /usr/bin/python /usr/local/bin/python

ENTRYPOINT [ "/docker_group.sh" ]
CMD ["/usr/bin/supervisord"]
