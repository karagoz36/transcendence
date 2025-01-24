FROM prom/alertmanager:latest

USER root

# Copy the Alertmanager configuration file
COPY conf/alertmanager.yml /etc/alertmanager/alertmanager.yml

# Copy the custom entrypoint script
COPY ./entrypoint.sh /usr/bin/entrypoint.sh

# Ensure the entrypoint script is executable
# RUN chmod +x /usr/bin/entrypoint.sh

USER root
# Set the entrypoint to the custom script
ENTRYPOINT ["/usr/bin/entrypoint.sh"]

# Set the working directory
WORKDIR /etc/alertmanager

# Default command to run Alertmanager
CMD ["--config.file=/etc/alertmanager/alertmanager.yml"]
# , \
# 	"--web.external-url=http://localhost:8000/alertmanager/", \
# 	"--web.route-prefix=/alertmanager/"]

