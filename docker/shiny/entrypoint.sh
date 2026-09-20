#!/bin/bash
set -e
# Shiny interno na 3839; nginx publica 3838 com frame-ancestors
sed -i 's/listen 3838;/listen 3839;/' /etc/shiny-server/shiny-server.conf || true
# se conf já tem 3838 no template original:
grep -q 'listen 3839' /etc/shiny-server/shiny-server.conf || \
  sed -i 's/listen 3838/listen 3839/' /etc/shiny-server/shiny-server.conf

ORIGIN="${DSN_FRAME_ANCESTORS:-http://localhost:8080}"
sed -i "s|http://localhost:8080|${ORIGIN}|g" /etc/nginx/sites-available/default

nginx
exec /usr/bin/shiny-server
