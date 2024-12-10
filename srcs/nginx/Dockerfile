FROM nginx:1.27.3
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt -subj "/CN=${DOMAIN_NAME}"
COPY default.conf /etc/nginx/conf.d/default.conf