FROM agaveapi/gridengine

RUN yum install -y docker-io \
  python

COPY docker_group.sh /docker_group.sh

RUN ln -s /usr/bin/python /usr/local/bin/python

RUN source /usr/share/gridengine/default/common/settings.sh && \
  echo "$HOSTNAME" > /usr/share/gridengine/default/common/act_qmaster && \
  /etc/init.d/sgemaster start && \
  qconf -rattr queue slots 10 debug

ENTRYPOINT [ "/docker_group.sh" ]
CMD ["/usr/bin/supervisord"]
