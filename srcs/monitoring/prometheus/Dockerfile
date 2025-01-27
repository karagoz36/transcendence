FROM prom/prometheus:latest

COPY /conf/prometheus.yml /etc/prometheus/prometheus.yml
COPY /conf/alertrules.yml /etc/prometheus/alertrules.yml

VOLUME ["/prometheus"]

WORKDIR /etc/prometheus

CMD ["--config.file=/etc/prometheus/prometheus.yml", \
     "--storage.tsdb.path=/prometheus", \
     "--storage.tsdb.retention.time=15d", \
     "--storage.tsdb.retention.size=5GB", \
     "--web.enable-lifecycle", \
     "--web.external-url=/prometheus", \
     "--web.route-prefix=/prometheus"]
