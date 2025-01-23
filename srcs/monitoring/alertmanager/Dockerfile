FROM prom/alertmanager:latest

COPY conf/alertmanager.yml /etc/alertmanager/alertmanager.yml

WORKDIR /etc/alertmanager

CMD ["--config.file=/etc/alertmanager/alertmanager.yml"]
# , \
# 	"--web.external-url=http://localhost:8000/alertmanager/", \
# 	"--web.route-prefix=/alertmanager/"]
