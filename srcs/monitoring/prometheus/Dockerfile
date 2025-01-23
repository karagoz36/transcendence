FROM prom/prometheus:latest

COPY /conf/prometheus.yml /etc/prometheus/prometheus.yml
COPY /conf/alertrules.yml /etc/prometheus/alertrules.yml


WORKDIR /etc/prometheus

CMD ["--config.file=/etc/prometheus/prometheus.yml", \
     "--storage.tsdb.path=/prometheus", \
     "--web.enable-lifecycle", \
     "--web.external-url=/prometheus", \
     "--web.route-prefix=/prometheus"]
