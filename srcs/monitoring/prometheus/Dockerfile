FROM prom/prometheus:latest

COPY /conf/prometheus.yml /etc/prometheus/prometheus.yml

WORKDIR /etc/prometheus

CMD ["--config.file=/etc/prometheus/prometheus.yml", \
     "--storage.tsdb.path=/prometheus", \
     "--web.enable-lifecycle", \
     "--web.external-url=/prometheus", \
     "--web.route-prefix=/prometheus"]
