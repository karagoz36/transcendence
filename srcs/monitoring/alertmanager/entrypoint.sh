#!/bin/bash

# # Fail on any error
# set -e

# # Path to the Alertmanager configuration file
# CONFIG_FILE="/etc/alertmanager/alertmanager.yml"

# # Check if EMAIL_HOST_USER and EMAIL_HOST_PASSWORD environment variables are set
# if [ -z "$EMAIL_HOST_USER" ] || [ -z "$EMAIL_HOST_PASSWORD" ]; then
#   echo "Environment variables EMAIL_HOST_USER and EMAIL_HOST_PASSWORD must be set."
#   exit 1
# fi

# # Replace placeholders in the configuration file with actual environment variable values
# sed -i "s|\${EMAIL_HOST_USER}|$EMAIL_HOST_USER|g" "$CONFIG_FILE"
# sed -i "s|\${EMAIL_HOST_PASSWORD}|$EMAIL_HOST_PASSWORD|g" "$CONFIG_FILE"

# # Execute the original entrypoint command
echo "HELLO"
exec "$@"
