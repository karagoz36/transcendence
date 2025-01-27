#!/bin/sh
set -e

CONFIG_FILE="/etc/alertmanager/alertmanager.yml"
TEMP_FILE="/tmp/alertmanager.yml"

if [ -z "$EMAIL_HOST_USER" ] || [ -z "$EMAIL_HOST_PASSWORD" ]; then
  echo "EMAIL_HOST_USER and EMAIL_HOST_PASSWORD must be set."
  exit 1
fi

sed -e "s|\${EMAIL_HOST_USER}|$EMAIL_HOST_USER|g" \
    -e "s|\${EMAIL_HOST_PASSWORD}|$EMAIL_HOST_PASSWORD|g" \
    "$CONFIG_FILE" > "$TEMP_FILE"

if [ ! -s "$TEMP_FILE" ]; then
  echo "Error: Empty config file after substitution"
  exit 1
fi

exec /bin/alertmanager \
  --config.file="$TEMP_FILE" \
  --cluster.advertise-address=:9093

