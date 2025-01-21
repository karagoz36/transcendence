FROM debian:bullseye-slim

ARG NODE_EXPORTER_VERSION=1.6.1

RUN apt-get update && \
    apt-get install -y --no-install-recommends wget ca-certificates procps && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /tmp

RUN wget https://github.com/prometheus/node_exporter/releases/download/v${NODE_EXPORTER_VERSION}/node_exporter-${NODE_EXPORTER_VERSION}.linux-amd64.tar.gz \
    && tar xfz node_exporter-${NODE_EXPORTER_VERSION}.linux-amd64.tar.gz \
    && mv node_exporter-${NODE_EXPORTER_VERSION}.linux-amd64/node_exporter /usr/local/bin/ \
    && rm -rf /tmp/*

# host /proc ve /sys directories

EXPOSE 9100

CMD ["/usr/local/bin/node_exporter", \
            "--collector.systemd", \
            "--collector.processes"]
