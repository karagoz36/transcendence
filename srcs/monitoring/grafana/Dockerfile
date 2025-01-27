FROM grafana/grafana:latest

USER root

COPY ./provisioning /etc/grafana/provisioning

EXPOSE 3000

CMD ["grafana-server", \
     "--homepath=/usr/share/grafana", \
     "--server.root_url=https://localhost:8000/grafana/", \
     "--server.serve_from_sub_path=true"]
