FROM prom/alertmanager:latest

USER root

COPY conf/alertmanager.yml /etc/alertmanager/alertmanager.yml
COPY entrypoint.sh /usr/bin/entrypoint.sh

RUN chmod +w /etc/alertmanager/alertmanager.yml && \
    chmod +x /usr/bin/entrypoint.sh

WORKDIR /etc/alertmanager

ENTRYPOINT ["/usr/bin/entrypoint.sh"]

