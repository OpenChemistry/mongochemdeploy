FROM agaveapi/gridengine

RUN yum install -y docker-io \
  python

COPY entrypoint.sh /entrypoint.sh

RUN ln -s /usr/bin/python /usr/local/bin/python

ENTRYPOINT [ "/entrypoint.sh" ]
CMD ["/usr/bin/supervisord"]
