FROM grafana/grafana:latest

# Ek eklentiler veya özelleştirmeler gerekiyorsa buraya eklenebilir
# Örneğin: RUN grafana-cli plugins install <plugin_name>

# COPY conf/grafana.ini /etc/grafana/grafana.ini

COPY ./provisioning /etc/grafana/provisioning


EXPOSE 3000

CMD ["grafana-server", \
     # "--config=/etc/grafana/grafana.ini", \
     "--homepath=/usr/share/grafana", \
     "--server.root_url=https://localhost:8000/grafana/", \
     "--server.serve_from_sub_path=true"]
